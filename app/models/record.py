from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

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
    eating_time: datetime = Field(default_factory=datetime.utcnow)

class FoodRecord(FoodRecordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

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
