from typing import List
from fastapi import APIRouter, Depends
from app.models.token import AccessToken
from app.db import db
from app.models.user import User, UserRead
from app.users import UserManager, current_active_user
from app.db import get_access_token_db, get_user_db

user_routes = APIRouter()

@user_routes.get("/list", tags=["users"], response_model=list[User], response_description="List of users")
async def list_users(quantity: int = 100) -> List[User]:
    ls = await UserManager.find_all().to_list(quantity)
    return ls



@user_routes.get("/db", tags=["db"], response_model=list[str])
async def list_db():
    ls = await db.list_collection_names()
    
    return ls

