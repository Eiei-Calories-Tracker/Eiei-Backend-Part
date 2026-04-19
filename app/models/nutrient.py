from pydantic import BaseModel
from models.enums import ActivityLevel, WeightTarget, Gender
from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
class user_information(BaseModel):
    weight: float
    height: float
    age: float
    activity_level: ActivityLevel
    target: WeightTarget
    gender: Gender
class nutrient(BaseModel):
    protein: float
    carb: float
    fat: float
    calories: float
class WeekNutritionRequest(BaseModel):
    user_id: int
    select_date : datetime
class calories_target_history(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    calories_target_per_day: float
    calories_target_per_week: float
    carb_target_per_day: float
    carb_target_per_week: float
    protein_target_per_day: float
    protein_target_per_week: float
    fat_target_per_day: float
    fat_target_per_week : float
    created_date: datetime
class CummulativeWeekNutrients(BaseModel):
    calories: float
    carb: float
    protein: float
    fat: float
   
class WeekNutritionResponse(BaseModel):
    cummulative_week_nutrients : CummulativeWeekNutrients
    cummulative_current_day_nutrients: CummulativeWeekNutrients
    target_week_nutrients: CummulativeWeekNutrients
    target_current_day_nutrients : CummulativeWeekNutrients
    current_date: datetime
    week_number: int
    day_state: int
    day: str
