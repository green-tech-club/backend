from beanie import PydanticObjectId
from fastapi_users import schemas
from fastapi_users.db import BeanieBaseUser

class User(BeanieBaseUser[PydanticObjectId]):
    name: str = None
    role: str = None

class UserRead(schemas.BaseUser[PydanticObjectId]):
    name: str = None
    role: str = None


class UserCreate(schemas.BaseUserCreate):
    name: str = None
    role: str = None


class UserUpdate(schemas.BaseUserUpdate):
    pass