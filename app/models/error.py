from fastapi_users.router.common import ErrorCode

class ExtendedErrorCode:
    def __init__(self):
        self.base_error_code = ErrorCode
        self.REGISTER_INVALID_INVITATION_EMAIL = "REGISTER_INVALID_INVITATION_EMAIL"
        self.INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
        self.USER_NOT_SUPERUSER = "USER_NOT_SUPERUSER"
        self.INVITATION_HAS_BEEN_SENT_ALREADY = "INVITATION_HAS_BEEN_SENT_ALREADY"

    def __getattr__(self, name):
        return getattr(self.base_error_code, name)

error_code = ExtendedErrorCode()