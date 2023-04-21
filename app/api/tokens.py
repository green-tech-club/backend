from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi_users.authentication.transport.base import Transport
from fastapi_users.authentication.strategy.base import Strategy
from fastapi_users.authentication.transport.bearer import BearerResponse
from pydantic import EmailStr
from app.models.token import AccessToken, InviteToken
from app.models.user import User, UserCreate
from app.users import current_active_user, get_user_manager, UserManager
from app.users import auth_backend

token_routes = APIRouter()

@token_routes.get("/tokens/list", tags=["auth"], response_model=list[AccessToken])
async def list_tokens():
    """its a temporary route which returns all tokens in the database"""
    ls = await AccessToken.find_all().to_list()
    return ls


@token_routes.get("/refresh_token", tags=["auth"], response_model=None,
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

def send_email(email: str, token: str):
    """ this function will send an email to the user with the token as a link,
        when the user clicks the link, the token will be validated and the user will be activated """
    pass

@token_routes.post('/send_invitation', tags=["auth"], response_model=InviteToken)
async def send_invitation(user_create: UserCreate, user: User = Depends(current_active_user), user_manager: UserManager = Depends(get_user_manager)):
    """ this route will generate a new token and save it in the database,
        then it will send an email to the user with the token as a link,
        when the user clicks the link, the token will be validated and the user will be activated """
    if user.is_superuser:
        newUser =await user_manager.create(user_create, safe=True, request=Request(scope={'type': 'http'}))
        # newUser = User(email=email, is_active=False, hashed_password="")
        await newUser.save()
        # token = InviteToken(user_id=newUser.id)
        # await token.save()
        await user_manager.request_verify(newUser, Request(scope={'type': 'http'}))
        # send_email(token, newUser.email)  # Added closing parenthesis here
    else:
        raise HTTPException(status_code=403, detail="You don't have enough permissions")

 