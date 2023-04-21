from typing import List
from fastapi import APIRouter, Depends
from app.db import db
from app.models.user import User


user_routes = APIRouter()

@user_routes.get("/list", tags=["users"], response_model=list[User], response_description="List of users")
async def list_users(quantity: int = 100) -> List[User]:
    """its a temporarly open route which returns all users in the database"""
    ls = await User.find_all().to_list(quantity)
    return ls



@user_routes.get("/db", tags=["db"], response_model=list[str])
async def list_db():
    """its a temporarly open route which returns all collections in the database"""
    ls = await db.list_collection_names()
    
    return ls


