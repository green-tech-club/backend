from typing import List
from fastapi import APIRouter, Depends
from app.models.token import AccessToken
from app.users import current_active_user

token_routes = APIRouter()

@token_routes.get("/tokens/list", tags=["auth"], response_model=list[AccessToken])
async def list_tokens():
    ls = await AccessToken.find_all().to_list()
    
    return ls

@token_routes.get("/refresh", tags=["auth"], response_model=AccessToken)
async def refresh_token(token: AccessToken = Depends(current_active_user)):
    """this function should refresh the token, update it in the database and return a new one"""
    return token