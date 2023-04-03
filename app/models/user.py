from beanie import PydanticObjectId
from fastapi_users import schemas

from beanie import PydanticObjectId
from fastapi_users.db import BeanieBaseUser

class User(BeanieBaseUser[PydanticObjectId]):
    pass

class UserRead(schemas.BaseUser[PydanticObjectId]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass