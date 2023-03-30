from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from .object import PyObjectId

from db.mongo import db
import bcrypt

# TODO: maybe we should implement more Pydantic models

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "password": "$2b$12$PQb5mqw"
            }
        }
    @staticmethod
    async def find_by_email(email):
        user = await db['users'].find_one({'email': email})
        return user
    
    
    async def save_new_user(self):
        user = jsonable_encoder(self)
        inserted = await db['users'].insert_one(user)
        return inserted



    def is_password_correct(entered_password, user_password):
        is_valid = bcrypt.checkpw(entered_password, user_password)
        return is_valid

class UpdateUserModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
            }
        }

class UserInDB(BaseModel):
    email: EmailStr

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
            }
        }