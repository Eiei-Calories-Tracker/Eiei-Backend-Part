from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from models.food import FoodNutrient, FoodNutrientRead

def get_thai_time():
    """Returns the current Thailand time (UTC+7) as a naive datetime"""
    return datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)

class FoodRecordBase(SQLModel):
    food_name: str
    sum_protein: float
    sum_fat: float
    sum_carb: float
    sum_calories: float
    quantity: float
    user_id: int = Field(foreign_key="useraccount.id")
    nutrition_id: Optional[int] = Field(default=None, foreign_key="foodnutrient.id")
    image_key: Optional[str] = None
    eating_time: datetime = Field(default_factory=get_thai_time)

class FoodRecord(FoodRecordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    food_nutrient: Optional[FoodNutrient] = Relationship()

class FoodRecordRead(SQLModel):
    food_record: FoodRecord
    food_nutrient: Optional[FoodNutrientRead] = None

class FoodRecordCreate(SQLModel):
    is_user_create: bool
    food_id: Optional[int] = None
    # Flat fields for new_food if is_user_create is true
    new_food_name: Optional[str] = None
    new_food_calories: Optional[float] = None
    new_food_carb: Optional[float] = None
    new_food_protein: Optional[float] = None
    new_food_fat: Optional[float] = None
    quantity: float
    eating_time: datetime
