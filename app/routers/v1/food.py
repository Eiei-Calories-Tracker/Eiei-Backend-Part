from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session, get_current_user
from models.account import UserAccount
from services import food_service

router = APIRouter(prefix="/food_nutrients", tags=["food"])

@router.get("/")
def get_all_food_nutrients(
    current_user: UserAccount = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Retrieve all food nutrients for the current user (System + User-specific)"""
    foods = food_service.retrieve_all_food_nutrients(session, current_user.id)
    
    # Format response as requested
    all_food_nutrients = [
        {
            "food_id": food.id,
            "food_name": food.food_name,
            "calories": food.calories,
            "carb": food.carb,
            "protein": food.protein,
            "fat": food.fat
        }
        for food in foods
    ]
    
    return {
        "data": {
            "all_food_nutrients": all_food_nutrients
        }
    }
