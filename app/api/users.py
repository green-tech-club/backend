from typing import List, Optional
from fastapi import Body, Depends, HTTPException, status, Request
from fastapi import APIRouter
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder

from models.user import UserModel, UpdateUserModel, UserInDB
from db.mongo import db
from .auth import get_current_user, get_password_hash

import uuid
import bcrypt

user_routes = APIRouter()

@user_routes.post("/signup", response_description="Add new user", status_code=201)
async def create_new_user(user_data: UserModel = Body(...)):
    try:
        user = await UserModel.find_by_email(user_data.email)
        if user:
            raise HTTPException(status_code=409, detail="This email already exists!")

        user_data.password = get_password_hash(user_data.password)
        insertion_result = await user_data.save_new_user()
        created_user = await db["users"].find_one({"_id": insertion_result.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)
    except Exception as e:
        print(e)
        return {'Error': 'Failed to create a new user'}





# def create_hashed_password(enterd_pass: str):
#     salt = bcrypt.gensalt()
#     hashed_pass = bcrypt.hashpw(enterd_pass.encode('utf-8'), salt)
#     return hashed_pass.decode('utf-8')

# @user_routes.post("/login", response_description="Endpoint for login for existing users")
# async def login(reqest: Request):
#     print('login')
#     try:
#         user = await UserModel.find_by_email(reqest._query_params['email'])
#         if (user): 
#             # check password
#             is_pass_valid = await UserModel.is_password_correct(reqest._query_params['password'].encode('utf-8'), user['password'].encode('utf-8'))
#             if (is_pass_valid):
#                 # generate token
#                 token = str(uuid.uuid4())
#                 # login succesfull
#                 return JSONResponse(status_code=200, 
#                 content={'message': 'successfully logged in', 'token': token})
#             else:
#                 return JSONResponse(status_code=403, content={'message': 'entered password is wrong'})
#         else:
#             return {'Error: user does not exist.'}
#     except Exception as e:
#         print(e)
#         return {'Error: failed to login'}


@user_routes.get("/list/users", response_description="List all (first 1000 actually) users", response_model=List[UserModel])
async def list_users():
    users = await db["users"].find().to_list(1000)
    return users

@user_routes.get("/users/{id}", response_description="Get a single user", response_model=UserModel)
async def get_user_by_id(id: str):
    print(await db["users"].find_one({"_id": id}))
    if (user := await db["users"].find_one({"_id": id})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"user {id} not found")


@user_routes.put("/users/{id}", response_description="update a user", response_model=UserModel)
async def update_user_by_id(id: str, user_data: UpdateUserModel=Body(...)):
    user = {k: v for k, v in user_data.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = await db["users"].update_one({"_id": id}, {"$set": user})

        if update_result.modified_count == 1:
            if (updated_user := await db["users"].find_one({"_id": id})) is not None:
                return updated_user
    if (existing_user := await db["users"].find_one({"_id": id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"user {id} not found")



@user_routes.delete("/users/{id}", response_description="Delete a user")
async def delete_user_by_id(id: str):
    delete_result = await db["users"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"user {id} not found")

