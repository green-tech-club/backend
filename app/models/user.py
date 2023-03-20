from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from .object import PyObjectId

from db.mongo import db
import bcrypt


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

    async def find_by_email(email):
        return await db['users'].find_one({'email': email})
    
    
    async def save_new_user(self):
        # self.create_hashed_password()
        # here was the problem, its inserted the object as a dict but the "_id" is not what we wanted but an ObjectId('yadayada') 
        # print(dict(vars(self)))
        user = jsonable_encoder(self)
        return await db['users'].insert_one(user)


    def create_hashed_password(self):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), salt)
        self.password = hashed_password.decode('utf-8')


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