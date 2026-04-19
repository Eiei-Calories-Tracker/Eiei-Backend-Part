from datetime import datetime, timedelta
import jwt
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS
from sqlmodel import Session, select
from models.account import UserAccount, UserAccountCreate, pwd_context
from typing import Optional

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_email(session: Session, email: str) -> Optional[UserAccount]:
    """Check if a user exists with the given email"""
    statement = select(UserAccount).where(UserAccount.email == email)
    return session.scalar(statement)

def create_user_account(session: Session, user_data: UserAccountCreate) -> UserAccount:
    """Create a new user account with hashed password"""
    hashed_password = pwd_context.hash(user_data.password)
    
    # Create the user object from the base data
    user_dict = user_data.model_dump(exclude={"password"})
    new_user = UserAccount(**user_dict, hashed_password=hashed_password)
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
