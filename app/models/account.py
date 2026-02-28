from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field
from passlib.context import CryptContext
from .enums import ActivityLevel, WeightTarget, Gender

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserAccountBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    gender: Gender
    activity_factor: ActivityLevel
    weight: float = Field(gt=0)  # kg
    height: float = Field(gt=0)  # cm
    target: WeightTarget
    birth_date: date

class UserAccount(UserAccountBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

class UserAccountCreate(UserAccountBase):
    password: str

class UserAccountRead(SQLModel):
    user_id: int

class LoginRequest(SQLModel):
    email: str
    password: str

class LoginResponse(SQLModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int

class UserAccountUpdate(SQLModel):
    activity_factor: Optional[ActivityLevel] = None
    weight: Optional[float] = Field(default=None, gt=0)
    height: Optional[float] = Field(default=None, gt=0)
    target: Optional[WeightTarget] = None

class UserProfileRead(UserAccountBase):
    pass
