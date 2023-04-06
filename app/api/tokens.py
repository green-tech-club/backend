from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_users.authentication.transport.base import Transport
from fastapi_users.authentication.strategy.base import Strategy
from app.models.token import AccessToken
from app.models.user import User
from app.users import current_active_user
from app.users import auth_backend

token_routes = APIRouter()

@token_routes.get("/tokens/list", tags=["auth"], response_model=list[AccessToken])
async def list_tokens():
    """its a temporary route which returns all tokens in the database"""
    ls = await AccessToken.find_all().to_list()
    return ls


@token_routes.get("/refresh_token", tags=["auth"])
async def refresh_token(user: User = Depends(current_active_user),strategy: Strategy = Depends(auth_backend.get_strategy)):
    """if the user logged in, this route will generate a new token than appends to the database,finally returns the token"""
    transport: Transport = auth_backend.transport
    token = await strategy.write_token(user)
    print(token)
    return await transport.get_login_response(token, Response())
 