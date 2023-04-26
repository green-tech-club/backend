
import uuid
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr

class InvitationCreate(BaseModel):
    email: EmailStr

class InvitationRead(BaseModel):
    code: str


class Invitation(Document):
    email: EmailStr
    code: str
    
    async def find_by_email(email: str):
        return await Invitation.find_one(Invitation.email == email)
    
    async def find_by_code(code: str):
        return await Invitation.find_one(Invitation.code == code)
    
    @classmethod
    async def create(cls, email: str):
        invitation = Invitation(email=email, code=str(uuid.uuid4()))
        await invitation.insert()
        return invitation

