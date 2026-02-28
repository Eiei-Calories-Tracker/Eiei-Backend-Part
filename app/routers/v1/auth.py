from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from db.database import get_session
from models.account import UserAccountCreate, UserAccountRead
from services import auth_service

router = APIRouter(prefix="/register", tags=["authentication"])

@router.post("/", response_model=UserAccountRead, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserAccountCreate,
    session: Session = Depends(get_session)
):
    """Register a new user account"""
    # 1. Check if user already exists
    existing_user = auth_service.get_user_by_email(session, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 2. Create new user
    new_user = auth_service.create_user_account(session, user_data)
    
    # 3. Return response in the requested format
    return {"user_id": new_user.id}
