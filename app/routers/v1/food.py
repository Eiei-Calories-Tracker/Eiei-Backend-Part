from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from dependencies import get_session, get_current_user
from models.account import UserAccount
from models.record import FoodRecordCreate, FoodRecord # Added FoodRecord
from services import food_service, ai_service, s3_service, food_record_service

router = APIRouter(prefix="", tags=["food"])

@router.get("/food_nutrients")
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

@router.post("/food_record")
async def create_food_record(
    is_user_create: bool = Form(...),
    food_id: Optional[int] = Form(None),
    new_food_name: Optional[str] = Form(None),
    new_food_calories: Optional[float] = Form(None),
    new_food_carb: Optional[float] = Form(None),
    new_food_protein: Optional[float] = Form(None),
    new_food_fat: Optional[float] = Form(None),
    quantity: float = Form(...),
    eating_time: str = Form(...),
    image: UploadFile = File(...),
    current_user: UserAccount = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Save a food log record with image upload to S3"""
    # 1. Upload image to S3
    image_key = await s3_service.upload_image_to_s3(image)
    
    # 2. Parse eating_time
    try:
        dt_eating_time = datetime.fromisoformat(eating_time.replace('Z', '+00:00'))
    except ValueError:
        dt_eating_time = datetime.utcnow()

    # 3. Prepare record data structure
    record_create = FoodRecordCreate(
        is_user_create=is_user_create,
        food_id=food_id,
        new_food_name=new_food_name,
        new_food_calories=new_food_calories,
        new_food_carb=new_food_carb,
        new_food_protein=new_food_protein,
        new_food_fat=new_food_fat,
        quantity=quantity,
        eating_time=dt_eating_time
    )
    
    # 4. Save record and calculate nutrients
    record = food_record_service.save_food_record(
        session, 
        current_user.id, 
        record_create, 
        image_key
    )
    
    return {
        "status": 201,
        "data": {
            "food_record_id": record.id
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

@router.patch("/food_record/{food_record_id}")
async def edit_food_record(
    food_record_id: int,
    quantity: Optional[float] = Form(None),
    eating_time: Optional[str] = Form(None),
    current_user: UserAccount = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update an existing food record (quantity/time) with nutrient recalculation"""
    # 1. Parse eating_time if provided
    dt_eating_time = None
    if eating_time:
        try:
            dt_eating_time = datetime.fromisoformat(eating_time.replace('Z', '+00:00'))
        except ValueError:
            pass

    # 2. Perform update
    updated_record = food_record_service.update_food_record(
        session,
        current_user.id,
        food_record_id,
        quantity=quantity,
        eating_time=dt_eating_time
    )
    
    if not updated_record:
        return {
            "status": 404,
            "message": "Food record not found or access denied"
        }
        
    return {
        "data": {
            "food_record_id": updated_record.id
        }
    }
