from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import Body, Depends, HTTPException, status, Request
from fastapi import APIRouter
from fastapi.responses import Response, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from models.user import UserModel, UpdateUserModel, UserInDB
from db.mongo import db
from config import config


SECRET_KEY = config.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(email: str, password: str):
    user = await db["users"].find_one({"email": email})
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return UserInDB(email=user["email"])

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(access_token):
    decoded_token = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
    return decoded_token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = UserInDB(email=email)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await db["users"].find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserModel(**user)


@user_routes.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_routes.post("/refresh_token")
async def refresh_token(access_token: str = Depends(oauth2_scheme)):
    """
    Endpoint to refresh the access token.
    """
    try:
        payload = decode_access_token(access_token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid access token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user = await UserModel.find_by_email(email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(data={"sub": user['email']}, expires_delta=access_token_expires)
    return {"access_token": new_access_token, "token_type": "bearer"}


@user_routes.get("/protected_route")
async def protected_route(current_user: UserModel = Depends(get_current_user)):
    return {"message": "This is a protected route!"}
