from fastapi_users_db_beanie.access_token import BeanieBaseAccessToken
from beanie import PydanticObjectId


class AccessToken(BeanieBaseAccessToken[PydanticObjectId]):  
    class Config:
        collection = "access_tokens"

