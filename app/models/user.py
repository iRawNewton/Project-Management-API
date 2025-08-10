from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict
import time

# Request schemas
class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Base user schema
class UserBase(BaseModel):
    orgId: str = "org123"
    name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    photoUrl: Optional[str] = None
    globalRole: str = "member"
    projectRoles: Dict[str, str] = {}
    status: str = "active"
    authProvider: str = "local"
    permissions: Dict[str, bool] = {
        "canApproveTimesheets": False,
        "canCreateProjects": False
    }
    timezone: str = "Asia/Kolkata"
    locale: str = "en-IN"
    createdAt: int = Field(default_factory=lambda: int(time.time() * 1000))
    lastSeenAt: Optional[int] = None
    invitedBy: Optional[str] = None

# For DB storage
class UserInDB(UserBase):
    hashed_password: str

# For API response (without password)
class UserPublic(UserBase):
    pass
