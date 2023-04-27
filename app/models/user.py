from beanie import PydanticObjectId
from fastapi_users import schemas
from fastapi_users.db import BeanieBaseUser

class User(BeanieBaseUser[PydanticObjectId]):
    first_name: str
    last_name: str
    country: str

       
                        
class UserRead(schemas.BaseUser[PydanticObjectId]):
    first_name: str
    last_name: str
    country: str



class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    country: str


class UserUpdate(schemas.BaseUserUpdate):
    password: str