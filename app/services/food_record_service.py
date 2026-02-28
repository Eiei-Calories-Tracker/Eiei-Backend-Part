from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlmodel import select
from models.record import FoodRecord, FoodRecordCreate
from models.food import FoodNutrient
from services import food_service

def save_food_record(
    session: Session, 
    user_id: int, 
    record_data: FoodRecordCreate, 
    image_key: str
) -> FoodRecord:
    """Calculate nutrients and save food record, optionally saving new food to catalog"""
    
    food_name = ""
    protein_per_unit = 0.0
    fat_per_unit = 0.0
    carb_per_unit = 0.0
    calories_per_unit = 0.0
    nutrition_id = record_data.food_id

    if record_data.is_user_create:
        # 1. Handle user-created food: Save to FoodNutrient first
        new_food = FoodNutrient(
            food_name=record_data.new_food_name,
            calories=record_data.new_food_calories,
            carb=record_data.new_food_carb,
            protein=record_data.new_food_protein,
            fat=record_data.new_food_fat,
            user_id=user_id
        )
        session.add(new_food)
        session.commit()
        session.refresh(new_food)
        
        nutrition_id = new_food.id
        food_name = new_food.food_name
        protein_per_unit = new_food.protein
        fat_per_unit = new_food.fat
        carb_per_unit = new_food.carb
        calories_per_unit = new_food.calories
    else:
        # 2. Handle system food: Fetch from DB
        food = session.get(FoodNutrient, record_data.food_id)
        if food:
            food_name = food.food_name
            protein_per_unit = food.protein
            fat_per_unit = food.fat
            carb_per_unit = food.carb
            calories_per_unit = food.calories
    
    # 3. Calculate totals
    qty = record_data.quantity
    record = FoodRecord(
        food_name=food_name,
        sum_protein=protein_per_unit * qty,
        sum_fat=fat_per_unit * qty,
        sum_carb=carb_per_unit * qty,
        sum_calories=calories_per_unit * qty,
        quantity=qty,
        user_id=user_id,
        nutrition_id=nutrition_id,
        image_key=image_key,
        eating_time=record_data.eating_time
    )
    
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

def update_food_record(
    session: Session,
    user_id: int,
    food_record_id: int,
    quantity: Optional[float] = None,
    eating_time: Optional[datetime] = None
) -> Optional[FoodRecord]:
    """Update food record and recalculate nutrients if quantity changes"""
    # 1. Fetch record and verify ownership
    record = session.get(FoodRecord, food_record_id)
    if not record or record.user_id != user_id:
        return None
    
    # 2. Update fields
    if eating_time is not None:
        record.eating_time = eating_time
        
    if quantity is not None:
        # Recalculate sums based on original unit nutrients
        # We get unit nutrients by dividing current sum by current quantity
        # Or more safely, fetch from FoodNutrient if nutrition_id exists
        if record.nutrition_id:
            food = session.get(FoodNutrient, record.nutrition_id)
            if food:
                record.sum_protein = food.protein * quantity
                record.sum_fat = food.fat * quantity
                record.sum_carb = food.carb * quantity
                record.sum_calories = food.calories * quantity
        else:
            # Fallback: simple ratio if nutrition_id is missing (should not happen usually)
            ratio = quantity / record.quantity if record.quantity > 0 else 0
            record.sum_protein *= ratio
            record.sum_fat *= ratio
            record.sum_carb *= ratio
            record.sum_calories *= ratio
            
        record.quantity = quantity
        
    session.add(record)
    session.commit()
    session.refresh(record)
    return record

def get_food_records_by_date(
    session: Session,
    user_id: int,
    target_date: datetime
) -> List[FoodRecord]:
    """Retrieve all food records for a specific user on a specific date (UTC)"""
    # Create start and end of the day in UTC
    start_of_day = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0)
    end_of_day = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59, 999999)

    statement = select(FoodRecord).where(
        FoodRecord.user_id == user_id,
        FoodRecord.eating_time >= start_of_day,
        FoodRecord.eating_time <= end_of_day
    ).order_by(FoodRecord.eating_time.asc())
    
    return session.scalars(statement).all()
