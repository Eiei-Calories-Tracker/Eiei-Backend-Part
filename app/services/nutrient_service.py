from models.enums import ActivityLevel, WeightTarget
from models.nutrient import nutrient, user_information, calories_target_history
from models.account import UserAccount
from sqlalchemy.orm import Session
from datetime import datetime
def calculate_calories_needed(information: user_information)->nutrient:
    BMR = 10 * information.weight + 6.25 * information.height - 5 * information.age
    if information.gender == "male":
        BMR += 5
    elif information.gender == "female":
        BMR -= 161
    factor = 1

    match information.activity_level:
        case ActivityLevel.SEDENTARY:
            factor = 1.2
        case ActivityLevel.LIGHTLY_ACTIVE:
            factor = 1.375
        case ActivityLevel.MODERATELY_ACTIVE:
            factor = 1.55
        case ActivityLevel.VERY_ACTIVE:
            factor = 1.725
        case ActivityLevel.EXTRA_ACTIVE:
            factor = 1.9
    TDEE = BMR * factor
    calories = TDEE
    match information.target:
        case WeightTarget.LOSE_WEIGHT:
            calories -= 300
        case WeightTarget.GAIN_WEIGHT:
            calories += 300
    protein_percentage = .25
    carb_percentage = .45
    fat_percentage = .30
    protein_g = calories * protein_percentage / 4
    carb_g = calories * carb_percentage / 4
    fat_g = calories * fat_percentage / 4
    return nutrient(calories=calories, carb=carb_g, fat=fat_g, protein=protein_g)

def add_calories_target(session: Session, user_id: int) -> None:
    
    user = session.get(UserAccount, user_id)
    if user is None:
        return
    today = datetime.today().date()
    birth_date = user.birth_date

    age = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
    information = user_information(
        weight=user.weight,
        height=user.height,
        age=age,
        gender=user.gender,
        activity_level=user.activity_factor,
        target=user.target
    )

    nutrient_data = calculate_calories_needed(information)
    
    calories_target = calories_target_history(
        user_id=user_id,
        calories_target_per_day=nutrient_data.calories,
        calories_target_per_week=nutrient_data.calories * 7,
        fat_target_per_day=nutrient_data.fat,
        fat_target_per_week=nutrient_data.fat * 7,
        protein_target_per_day=nutrient_data.protein,
        protein_target_per_week=nutrient_data.protein * 7,
        carb_target_per_day=nutrient_data.carb,
        carb_target_per_week=nutrient_data.carb * 7,
        created_date=datetime.now()
    )
    
    session.add(calories_target)
    session.commit()
    
