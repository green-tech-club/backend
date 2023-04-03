from fastapi import APIRouter, Depends
from app.models.token import AccessToken
from app.db import db
from app.models.user import User
from app.schemas.user import UserRead
from app.users import current_active_user


list_any = APIRouter()

@list_any.get("/users", tags=["users"], response_model=list[User], response_description="List of users")
async def list_users():
    ls = await User.find_all().to_list()
    
    return ls

@list_any.get("/tokens", tags=["tokens"], response_model=list[AccessToken])
async def list_tokens():
    ls = await AccessToken.find_all().to_list()
    
    return ls

@list_any.get("/db", tags=["db"], response_model=list[str])
async def list_db():
    ls = await db.list_collection_names()
    
    return ls

