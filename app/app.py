from beanie import init_beanie
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.report_storage import report_routes
from app.db.db import User, AccessToken, db
from app.models.report_storage import Report
from app.models.user import UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users
from app.api.users import user_routes
from app.api.auth import auth_routes
from app.models.invitation import Invitation
app = FastAPI()

origins = [
           "http://localhost:8000",
           "http://localhost:3000",
           "https://unpap.herokuapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"]
)
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
#     dependencies=[Depends(verify_invitation_email)],
# )
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(report_routes, prefix="/reports", tags=["reports"])

app.include_router(user_routes, prefix="/user", tags=["users"])

app.include_router(auth_routes, prefix="/auth", tags=["auth"])

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

@app.get("/healthcheck")
async def healthcheck():
    return {"message": "OK", "status": 200}

    




@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
            AccessToken,
            Report,
            Invitation,
        ],
    )