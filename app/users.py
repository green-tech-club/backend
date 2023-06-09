from typing import Optional

from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
)
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin

from app.db.db import User, AccessToken, get_user_db, get_access_token_db, get_invite_token_db
from app.models.invitation import Invitation
from app.settings import settings

SECRET = settings.secret_key


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        try:
            deleted = await Invitation.delete(await Invitation.find_by_email(user.email))
            if deleted:
                deleted = user.email
        except:
            deleted = 0
        print(f"User {user.id} has registered.\nDeleted invitation code from the database, for email: {deleted}")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


transport = BearerTransport(tokenUrl="auth/login")
# transport = CookieTransport(cookie_max_age=3600)

# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=settings.token_lifetime)

auth_backend = AuthenticationBackend(
    name="database",
    transport=transport,
    get_strategy=get_database_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
