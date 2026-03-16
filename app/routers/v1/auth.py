from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from dependencies import get_session
from models.account import UserAccountCreate, UserAccountRead, LoginRequest, LoginResponse
from services import auth_service, nutrient_service
router = APIRouter(prefix="", tags=["authentication"]) # Removed prefix 'register' to accommodate both

@router.post("/register", response_model=UserAccountRead, status_code=status.HTTP_201_CREATED)
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
    
    # add food nutrition record
    nutrient_service.add_calories_target(session, new_user.id)
    # 3. Return response in the requested format
    return {"user_id": new_user.id}


@router.post("/login", response_model=LoginResponse)
def login_user(
    login_data: LoginRequest,
    session: Session = Depends(get_session)
):
    """Authenticate user and return access token"""
    # 1. Get user by email
    user = auth_service.get_user_by_email(session, login_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # 2. Verify password
    if not auth_service.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # 3. Create access token
    access_token = auth_service.create_access_token(data={"sub": user.email, "user_id": user.id})
    
    # 4. Return response
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id
    }
