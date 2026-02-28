from fastapi import APIRouter, Depends
from sqlmodel import Session
from models.account import UserAccount, UserAccountUpdate
from services import user_service
from dependencies import get_current_user, get_session

router = APIRouter(prefix="/users", tags=["users"])

@router.patch("/")
def update_profile(
    update_data: UserAccountUpdate,
    current_user: UserAccount = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update current user profile"""
    updated_user = user_service.update_user_profile(session, current_user, update_data)
    
    # Returning the requested specific structure
    return {
        "data": {
            "user_id": updated_user.id,
            "activity_factor": updated_user.activity_factor,
            "weight": updated_user.weight,
            "height": updated_user.height,
            "target": updated_user.target
        }
    }


@router.get("/")
def get_profile(current_user: UserAccount = Depends(get_current_user)):
    """Retrieve current user profile"""
    return {
        "data": {
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "gender": current_user.gender,
            "activity_factor": current_user.activity_factor,
            "weight": current_user.weight,
            "height": current_user.height,
            "target": current_user.target,
            "birth_date": current_user.birth_date
        }
    }
