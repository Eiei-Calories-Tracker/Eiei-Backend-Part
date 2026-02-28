from sqlmodel import Session, select
from models.account import UserAccount, UserAccountCreate, pwd_context
from typing import Optional

def get_user_by_email(session: Session, email: str) -> Optional[UserAccount]:
    """Check if a user exists with the given email"""
    statement = select(UserAccount).where(UserAccount.email == email)
    return session.exec(statement).first()

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
