from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from dependencies import get_session, get_current_user
from models.account import UserAccount
from services import food_service, ai_service

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

@router.post("/food_name")
async def predict_food(
    image: UploadFile = File(...),
    current_user: UserAccount = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Predict food name from image and return nutritional data"""
    # 1. Get prediction from AI
    ai_result = await ai_service.predict_food_from_image(image)
    
    if not ai_result:
        return {
            "status": 500,
            "message": "AI Prediction service failed"
        }
    
    food_name = ai_result.get("best_prediction")
    confidence = ai_result.get("best_confidence")
    
    # 2. Lookup nutrients in our DB
    food_record = food_service.get_food_by_name(session, food_name)
    
    # 3. Format response (Option A: food_id: null and 0 nutrients if not found)
    nutrients = {
        "calories": 0.0,
        "carb": 0.0,
        "protein": 0.0,
        "fat": 0.0
    }
    food_id = None
    
    if food_record:
        food_id = food_record.id
        nutrients = {
            "calories": food_record.calories,
            "carb": food_record.carb,
            "protein": food_record.protein,
            "fat": food_record.fat
        }
    
    return {
        "data": {
            "food_id": food_id,
            "food_name": food_name,
            "nutrients": nutrients,
            "confidence_score": confidence
        }
    }
