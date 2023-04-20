from bson import ObjectId
from app.db.db import db_users, db_tokens
from app.models.user import User
from app.models.token import AccessToken


async def get_user_by_id(user_id: str):
    """Get a user from the database by its id"""
    user = await db_users.find_one({"_id": user_id})
    return user


async def get_user_by_email(email: str):
    """Get a user from the database by its email"""
    user = await db_users.find_one({"email": email})
    return user


async def get_user_id_by_token(token: str):
    """Get a user from the database by its username"""
    access_token: AccessToken = await db_tokens.find_one({"token": token})
    print(access_token)
    user_id: ObjectId = access_token.get("user_id")
    return user_id
