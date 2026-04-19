from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlmodel import select
from models.food import FoodNutrient
from typing import List, Optional

def retrieve_all_food_nutrients(session: Session, user_id: int) -> List[FoodNutrient]:
    """Retrieve system foods (user_id is NULL) and specific user foods"""
    statement = select(FoodNutrient).where(
        or_(
            FoodNutrient.user_id == None,
            FoodNutrient.user_id == user_id
        )
    )
    return session.scalars(statement).all()

def get_food_by_name(session: Session, food_name: str) -> Optional[FoodNutrient]:
    """Find a food item by its name (exact match, system first)"""
    if food_name == "":
        return FoodNutrient(
            food_name="",
            calories=.0,
            carb=.0,
            protein=.0,
            fat=.0
        )
    statement = select(FoodNutrient).where(FoodNutrient.food_name == food_name).order_by(FoodNutrient.user_id.isnot(None))
    return session.scalar(statement)
