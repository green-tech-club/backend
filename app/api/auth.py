from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_users.authentication.transport.base import Transport
from fastapi_users.authentication.strategy.base import Strategy
from fastapi_users.router.common import ErrorModel
from fastapi_users import exceptions
from app.models.user import User, UserCreate, UserRead
from app.models.invitation import InvitationCreate, Invitation, InvitationRead
from app.models.error import error_code
from app.users import UserManager, current_active_user, get_user_manager
from app.models.token import AccessToken
from app.models.user import User, UserCreate
from app.users import current_active_user, get_user_manager, UserManager
from app.users import auth_backend
from tools.send_email import send_email

auth_routes = APIRouter()

@auth_routes.get("/tokens/list", tags=["auth"], response_model=list[AccessToken])
async def list_tokens():
    """its a temporary route which returns all tokens in the database"""
    ls = await AccessToken.find_all().to_list()
    return ls


@auth_routes.get("/refresh_token", tags=["auth"], response_model=None,
                  responses={status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."},
                             status.HTTP_200_OK: {"model": None}})
async def refresh_token(user: User = Depends(current_active_user),
                        strategy: Strategy = Depends(auth_backend.get_strategy)):
    """ if the user logged in, this route based on the authentication strategy and transport type,
        it will generate a new token and depending on the strategy will save the token,
        finally returns the token. """
    transport: Transport = auth_backend.transport
    token = await strategy.write_token(user)
    return await transport.get_login_response(token, Response())


 
async def verify_invitation(invitation: InvitationRead):
    """
    Verify if the provided invitation code exists in the database. Raise an HTTPException with status code 403 (Forbidden) if not found.
    """
    inv = await Invitation.find_by_code(invitation.code)
    if not inv:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error_code.INVALID_CREDENTIALS)
    print(f'found invitation: {inv}')
    return inv


@auth_routes.post("/is-invitation-valid")
async def is_invitation_valid(invitation: Invitation = Depends(verify_invitation)):
    """
    Check if the provided invitation is valid and return its status and associated email.
    """
    verified_invitation = await Invitation.find_by_code(invitation.code)
    return {"status": "valid", "email": verified_invitation.email}

@auth_routes.post("/send-invitation",responses={
                                                status.HTTP_400_BAD_REQUEST: {
                                                    "model": ErrorModel,
                                                    "content": {
                                                        "application/json": {
                                                            "examples": {
                                                                error_code.REGISTER_USER_ALREADY_EXISTS: {
                                                                    "summary": "A user with this email already exists.",
                                                                    "value": {
                                                                        "detail": error_code.REGISTER_USER_ALREADY_EXISTS
                                                                    }},
                                                                error_code.USER_NOT_SUPERUSER: {
                                                                    "summary": "Only superusers can send invitations.",
                                                                    "value": {
                                                                        "detail": error_code.USER_NOT_SUPERUSER
                                                                    }},
                                                                error_code.INVITATION_HAS_BEEN_SENT_ALREADY: {
                                                                    "summary": "Invitation to this email has benn sent already.",
                                                                    "value": {
                                                                        "detail": error_code.INVITATION_HAS_BEEN_SENT_ALREADY
                                                                    }},
                                                                }}}}})


async def send_invitation(invitation: InvitationCreate,
                          user: User = Depends(current_active_user),
                          manager: UserManager = Depends(get_user_manager)):
    """
    Send an invitation to the specified email. Only superusers are allowed to send invitations.\
    Raise an HTTPException with status code 400 (Bad Request) if the email is already registered, or 403 (Forbidden) if the user is not a superuser.
    """
    if user.is_superuser:
        
        if await Invitation.find_by_email(invitation.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_code.INVITATION_HAS_BEEN_SENT_ALREADY,
            )
        try:
            if await manager.get_by_email(invitation.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_code.REGISTER_USER_ALREADY_EXISTS,
                )
        except exceptions.UserNotExists:
            invitation = await Invitation.create(email=invitation.email)
            send_email(to_emails=invitation.email,subject="Invitation to Greentech!" ,html_content=f"Your invitation code: {invitation.code}")
            return {"invitation_code": invitation.code}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_code.USER_NOT_SUPERUSER
        )

    
@auth_routes.post("/list/invitation", response_model=list[Invitation])
async def list_invitations(user: User = Depends(current_active_user)):
    """
    List all invitations. Only superusers are allowed to access this route.\
    Raise an HTTPException with status code 403 (Forbidden) if the user is not a superuser.
    """
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_code.USER_NOT_SUPERUSER
        )
    invitations = await Invitation.find_all().to_list()
    return invitations


@auth_routes.post("/register",
        response_model=UserRead,
        status_code=status.HTTP_201_CREATED,
        name="register:register",
        responses={
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            error_code.REGISTER_USER_ALREADY_EXISTS: {
                                "summary": "A user with this email already exists.",
                                "value": {
                                    "detail": error_code.REGISTER_USER_ALREADY_EXISTS
                                },
                            },
                            error_code.REGISTER_INVALID_PASSWORD: {
                                "summary": "Password validation failed.",
                                "value": {
                                    "detail": {
                                        "code": error_code.REGISTER_INVALID_PASSWORD,
                                        "reason": "Password should be"
                                        "at least 3 characters",
                                    }
                                },
                            },
                            error_code.REGISTER_INVALID_INVITATION_EMAIL:{
                                "summary": "Email does not match invitation email.",
                                "value": {
                                    "detail": {
                                        "code": error_code.REGISTER_INVALID_INVITATION_EMAIL,
                                        "reason": "Email does not match invitation email.",
                                    }
                            },
                        }
                    }
                },
            },
        },}
    )


async def register( request: Request, user: UserCreate,
                    invitation: InvitationRead = Depends(verify_invitation), 
                    manager: UserManager = Depends(get_user_manager)):
    """
    Register a new user with the provided information and the valid invitation. \
    Raise an HTTPException with status code 400 (Bad Request) if the email doesn't match the invitation email,\
    if the email is already registered, or if the password validation fails.
    """
    verified_invitation = await Invitation.find_by_code(invitation.code)
    if user.email != verified_invitation.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_code.REGISTER_INVALID_INVITATION_EMAIL)
    else:
        try:
            created_user = await manager.create(
                user, safe=True, request=request
            )
        except exceptions.UserAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_code.REGISTER_USER_ALREADY_EXISTS,
            )
        except exceptions.InvalidPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": error_code.REGISTER_INVALID_PASSWORD,
                    "reason": e.reason,
                },
            )

        return UserRead.from_orm(created_user)
