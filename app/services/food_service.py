from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlmodel import select
from models.food import FoodNutrient
from typing import List

def retrieve_all_food_nutrients(session: Session, user_id: int) -> List[FoodNutrient]:
    """Retrieve system foods (user_id is NULL) and specific user foods"""
    statement = select(FoodNutrient).where(
        or_(
            FoodNutrient.user_id == None,
            FoodNutrient.user_id == user_id
        )
    )
    return session.scalars(statement).all()
