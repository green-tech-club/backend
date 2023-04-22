import motor.motor_asyncio
from app.settings import settings
from fastapi_users.db import BeanieUserDatabase
from fastapi_users_db_beanie.access_token import BeanieAccessTokenDatabase
from app.models.user import User
from app.models.token import AccessToken, InviteToken

db_user = settings.db_username
db_password = settings.db_password
db_cluster = settings.db_cluster

MONGODB_URL = f"mongodb+srv://{db_user}:{db_password}@{db_cluster}vwuw.mongodb.net/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.college


async def get_user_db():
    yield BeanieUserDatabase(User)


async def get_access_token_db():
    yield BeanieAccessTokenDatabase(AccessToken)

async def get_invite_token_db():  
    yield BeanieAccessTokenDatabase(InviteToken)