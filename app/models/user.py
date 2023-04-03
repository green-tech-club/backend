from beanie import PydanticObjectId
from fastapi_users.db import BeanieBaseUser

class User(BeanieBaseUser[PydanticObjectId]):
    pass