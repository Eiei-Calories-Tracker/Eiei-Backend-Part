from typing import Optional
from sqlmodel import SQLModel, Field

class FoodNutrientBase(SQLModel):
    food_name: str = Field(index=True)
    calories: float
    carb: float
    protein: float
    fat: float
    user_id: Optional[int] = Field(default=None, foreign_key="useraccount.id")

class FoodNutrient(FoodNutrientBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class FoodNutrientRead(SQLModel):
    food_id: int
    food_name: str
    calories: float
    carb: float
    protein: float
    fat: float
