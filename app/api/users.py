from typing import List, Optional
from fastapi import Body, HTTPException, status
from fastapi import APIRouter
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder

from models.user import UserModel, UpdateUserModel
from db.mongo import db

user_routes = APIRouter()

@user_routes.post("/users", response_description="Add new user", response_model=UserModel)
async def create_new_user(user_data: UserModel = Body(...)):
    user = jsonable_encoder(user_data)
    new_user = await db["users"].insert_one(user)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@user_routes.get("/users", response_description="List all (first 1000 actually) users", response_model=List[UserModel])
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
