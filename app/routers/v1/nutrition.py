from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlmodel import select
from dependencies import get_session
from datetime import date, timedelta, datetime
from models.nutrient import WeekNutritionRequest, calories_target_history, WeekNutritionResponse, CummulativeWeekNutrients
from models.record import FoodRecord
from services import nutrient_service
from models.account import UserAccount
from collections import defaultdict
router = APIRouter(prefix="", tags=["nutrition"])


@router.get("/nutrients/{user_id}/{date}")
async def get_week_nutrition(
    user_id: int,
    date: date,
    session: Session = Depends(get_session)
) -> list[WeekNutritionResponse]:
    result: list[WeekNutritionResponse] = []
    target_date = date
    week_list = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    weekday = target_date.weekday()
    start_of_week = target_date - timedelta(days=(weekday + 1) % 7)
    end_of_week = start_of_week + timedelta(days=6)

    find_user_statement = select(UserAccount.created_date).where(UserAccount.id == user_id)
    query_result = session.execute(find_user_statement).scalars().first()

    

    food_range_statement = (
        select(
            func.date(FoodRecord.eating_time).label("day"),
            func.sum(FoodRecord.sum_calories * FoodRecord.quantity).label("calories"),
            func.sum(FoodRecord.sum_protein * FoodRecord.quantity).label("protein"),
            func.sum(FoodRecord.sum_carb * FoodRecord.quantity).label("carb"),
            func.sum(FoodRecord.sum_fat * FoodRecord.quantity).label("fat")
        )
        .where(
            func.date(FoodRecord.eating_time) >= func.date(start_of_week),
            func.date(FoodRecord.eating_time) <= func.date(end_of_week),
            FoodRecord.user_id == user_id
        )
        .group_by(func.date(FoodRecord.eating_time))
        .order_by(func.date(FoodRecord.eating_time))
    )

    food_result = session.execute(food_range_statement).all()
    food_map = {row.day: row for row in food_result}

    
    prev_statement = (
        select(calories_target_history)
        .where(func.date(calories_target_history.created_date) < func.date(start_of_week),
               calories_target_history.user_id == user_id)
        .order_by(calories_target_history.created_date.desc())
        .limit(1)
    )
    range_statement = (
        select(calories_target_history)
        .where(
            func.date(calories_target_history.created_date) >= func.date(start_of_week),
            func.date(calories_target_history.created_date) <= func.date(end_of_week),
            calories_target_history.user_id == user_id
        )
        .order_by(calories_target_history.created_date.desc())
    )

    prev_result : calories_target_history = session.execute(prev_statement).scalars().first()
    range_result : list[calories_target_history] = session.execute(range_statement).scalars().all()
    day_rows_map = defaultdict(list)
    for row in range_result:
        day_key = row.created_date.day
        day_rows_map[day_key].append(row)

    latest_per_day = {}
    for day, rows in day_rows_map.items():
        latest_row = max(rows, key=lambda r: r.created_date)
        latest_per_day[day] = latest_row
    range_map = {row.created_date.day : row for row in range_result}
    if prev_result is not None:
        range_map[-1] = prev_result
    elif len(range_map) > 0:
        min_day = min(range_map.keys())
        range_map[-1] = range_map[min_day]
    
    
    
    cum_calories = 0.0
    cum_protein = 0.0
    cum_carb = 0.0
    cum_fat = 0.0
    if range_map.get(-1) is None:
        upper_statement = select(calories_target_history).where(func.date(calories_target_history.created_date) > func.date(end_of_week), calories_target_history.user_id == user_id).order_by(calories_target_history.created_date).limit(1)
        upper_result = session.execute(upper_statement).scalars().first()
        if upper_result is None:
            nutrient_service.add_calories_target(session, user_id)
            new_row = session.execute(
                select(calories_target_history)
                .order_by(calories_target_history.created_date.desc())
                .limit(1)
            ).scalars().first()
            range_map[-1] = new_row
        else:
            range_map[-1] = upper_result
    
    for i in range(7):
        current_date = start_of_week + timedelta(days=i)
        
        day_key = current_date.day

        lower_possible_keys = [k for k in range_map.keys() if k <= day_key]
        upper_possible_keys = [k for k in range_map.keys() if k >= day_key]
        
        
        nearest_key_lower = max(lower_possible_keys) if lower_possible_keys else -1
        nearest_key_upper = min(upper_possible_keys) if upper_possible_keys else -1
        # print("nearest_key_upper", nearest_key_upper)
        # print("nearest_key_lower", nearest_key_lower)
        limit_row_per_day = latest_per_day.get(day_key)
        if not limit_row_per_day:
            limit_row_per_day = range_map.get(nearest_key_lower)
        limit_row_per_week = range_map.get(nearest_key_upper)
        data = food_map.get(current_date)
        calories = round(data.calories, 2) if data else 0
        protein = round(data.protein, 2) if data else 0
        carb = round(data.carb, 2) if data else 0
        fat = round(data.fat, 2) if data else 0
        cum_calories += calories
        cum_protein += protein
        cum_carb += carb
        cum_fat += fat
        week_result = (current_date - query_result.date()).days // 7
        result.append(
            WeekNutritionResponse(
                cummulative_week_nutrients=CummulativeWeekNutrients(
                    calories=round(cum_calories, 2),
                    protein=round(cum_protein, 2),
                    carb=round(cum_carb, 2),
                    fat=round(cum_fat, 2),
                ),
                cummulative_current_day_nutrients=CummulativeWeekNutrients(
                    calories=round(calories, 2),
                    protein=round(protein, 2),
                    carb=round(carb, 2),
                    fat=round(fat, 2),
                ),
                target_week_nutrients=CummulativeWeekNutrients(
                    calories=round(limit_row_per_week.calories_target_per_week, 2) if limit_row_per_week else 0,
                    protein=round(limit_row_per_week.protein_target_per_week, 2) if limit_row_per_week else 0,
                    carb=round(limit_row_per_week.carb_target_per_week, 2) if limit_row_per_week else 0,
                    fat=round(limit_row_per_week.fat_target_per_week, 2) if limit_row_per_week else 0,
                ),
                target_current_day_nutrients=CummulativeWeekNutrients(
                    calories=round(limit_row_per_day.calories_target_per_day, 2) if limit_row_per_day else 0,
                    protein=round(limit_row_per_day.protein_target_per_day, 2) if limit_row_per_day else 0,
                    carb=round(limit_row_per_day.carb_target_per_day, 2) if limit_row_per_day else 0,
                    fat=round(limit_row_per_day.fat_target_per_day, 2) if limit_row_per_day else 0,
                ),
                current_date=current_date,
                week_number = (week_result + 1) if query_result and week_result >= 0 else 0,
                day_state = (
                    1
                    if limit_row_per_day
                    and calories <= round(limit_row_per_day.calories_target_per_day*1.10, 2) and calories >= round(limit_row_per_day.calories_target_per_day*0.90, 2)
                    and protein <= round(limit_row_per_day.protein_target_per_day*1.10, 2) and protein >= round(limit_row_per_day.protein_target_per_day*0.90, 2)
                    and carb <= round(limit_row_per_day.carb_target_per_day*1.10, 2) and carb >= round(limit_row_per_day.carb_target_per_day*0.90, 2)
                    and fat <= round(limit_row_per_day.fat_target_per_day*1.10, 2) and fat >= round(limit_row_per_day.fat_target_per_day*0.90, 2)
                    else 2
                    if current_date == datetime.now().date()
                    else 0
                ),
                day=week_list[i]
            )
        )
    return result
    
    
    