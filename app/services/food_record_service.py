from sqlalchemy.orm import Session
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
