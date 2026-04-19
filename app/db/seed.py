from sqlalchemy.orm import Session
from sqlmodel import select
from models.food import FoodNutrient

FOOD_DATA = [
    {"food_name": "BitterMelonSoup", "calories": 200, "carb": 10, "protein": 18, "fat": 12},
    {"food_name": "BooPadPongali", "calories": 450, "carb": 15, "protein": 25, "fat": 32},
    {"food_name": "CurriedFishCake", "calories": 240, "carb": 12, "protein": 15, "fat": 15},
    {"food_name": "Dumpling", "calories": 180, "carb": 15, "protein": 12, "fat": 8},
    {"food_name": "EggsStewed", "calories": 210, "carb": 12, "protein": 14, "fat": 12},
    {"food_name": "FriedChicken", "calories": 300, "carb": 10, "protein": 22, "fat": 20},
    {"food_name": "FriedKale", "calories": 400, "carb": 12, "protein": 18, "fat": 30},
    {"food_name": "FriedMusselPancakes", "calories": 550, "carb": 45, "protein": 15, "fat": 35},
    {"food_name": "GaengJued", "calories": 120, "carb": 5, "protein": 10, "fat": 6},
    {"food_name": "GaengKeawWan", "calories": 350, "carb": 15, "protein": 18, "fat": 25},
    {"food_name": "GaiYang", "calories": 210, "carb": 2, "protein": 25, "fat": 12},
    {"food_name": "GoongObWoonSen", "calories": 300, "carb": 40, "protein": 20, "fat": 8},
    {"food_name": "GoongPao", "calories": 120, "carb": 1, "protein": 24, "fat": 2},
    {"food_name": "GrilledSquid", "calories": 150, "carb": 2, "protein": 28, "fat": 3},
    {"food_name": "HoyKraeng", "calories": 70, "carb": 2, "protein": 12, "fat": 1},
    {"food_name": "HoyLaiPrikPao", "calories": 230, "carb": 10, "protein": 12, "fat": 15},
    {"food_name": "Joke", "calories": 320, "carb": 45, "protein": 15, "fat": 10},
    {"food_name": "KaiJeowMooSaap", "calories": 450, "carb": 3, "protein": 18, "fat": 40},
    {"food_name": "KaiThoon", "calories": 120, "carb": 3, "protein": 12, "fat": 8},
    {"food_name": "KaoManGai", "calories": 580, "carb": 65, "protein": 22, "fat": 25},
    {"food_name": "KaoMooDang", "calories": 540, "carb": 70, "protein": 18, "fat": 22},
    {"food_name": "KhanomJeenNamYaKati", "calories": 350, "carb": 45, "protein": 12, "fat": 15},
    {"food_name": "KhaoMokGai", "calories": 600, "carb": 75, "protein": 20, "fat": 24},
    {"food_name": "KhaoMooTodGratiem", "calories": 620, "carb": 70, "protein": 20, "fat": 30},
    {"food_name": "KhaoNiewMaMuang", "calories": 450, "carb": 80, "protein": 5, "fat": 12},
    {"food_name": "KkaoKlukKaphi", "calories": 510, "carb": 65, "protein": 15, "fat": 20},
    {"food_name": "KorMooYang", "calories": 320, "carb": 2, "protein": 18, "fat": 28},
    {"food_name": "KuaKling", "calories": 180, "carb": 5, "protein": 25, "fat": 8},
    {"food_name": "KuayJab", "calories": 400, "carb": 45, "protein": 18, "fat": 16},
    {"food_name": "KuayTeowReua", "calories": 200, "carb": 25, "protein": 10, "fat": 8},
    {"food_name": "LarbMoo", "calories": 170, "carb": 6, "protein": 22, "fat": 8},
    {"food_name": "MassamanGai", "calories": 450, "carb": 25, "protein": 20, "fat": 32},
    {"food_name": "MooSatay", "calories": 300, "carb": 10, "protein": 20, "fat": 20},
    {"food_name": "NamTokMoo", "calories": 180, "carb": 6, "protein": 22, "fat": 8},
    {"food_name": "PadPakBung", "calories": 120, "carb": 8, "protein": 3, "fat": 9},
    {"food_name": "PadPakRuamMit", "calories": 130, "carb": 10, "protein": 4, "fat": 10},
    {"food_name": "PadThai", "calories": 550, "carb": 75, "protein": 15, "fat": 22},
    {"food_name": "PadYordMala", "calories": 120, "carb": 8, "protein": 3, "fat": 9},
    {"food_name": "PhatKaphrao", "calories": 580, "carb": 70, "protein": 20, "fat": 25},
    {"food_name": "PorkStickyNoodles", "calories": 480, "carb": 65, "protein": 15, "fat": 18},
    {"food_name": "Roast_duck", "calories": 280, "carb": 3, "protein": 22, "fat": 20},
    {"food_name": "Roast_fish", "calories": 180, "carb": 0, "protein": 35, "fat": 4},
    {"food_name": "Somtam", "calories": 80, "carb": 18, "protein": 3, "fat": 1},
    {"food_name": "SonInLawEggs", "calories": 280, "carb": 25, "protein": 14, "fat": 12},
    {"food_name": "StewedPorkLeg", "calories": 600, "carb": 70, "protein": 22, "fat": 25},
    {"food_name": "Suki", "calories": 280, "carb": 30, "protein": 25, "fat": 6},
    {"food_name": "TomKhaGai", "calories": 300, "carb": 12, "protein": 18, "fat": 22},
    {"food_name": "TomYumGoong", "calories": 250, "carb": 10, "protein": 20, "fat": 15},
    {"food_name": "YamWoonSen", "calories": 220, "carb": 35, "protein": 15, "fat": 5},
    {"food_name": "Yentafo", "calories": 320, "carb": 45, "protein": 15, "fat": 8},
]

def seed_food_nutrients(session: Session):
    """Seed the database with initial food nutrient data if empty"""
    # Check if table is empty
    statement = select(FoodNutrient)
    existing_count = len(session.execute(statement).all())
    
    if existing_count == 0:
        print("Seeding food nutrient data...")
        for data in FOOD_DATA:
            food = FoodNutrient(**data)
            session.add(food)
        session.commit()
        print(f"Successfully seeded {len(FOOD_DATA)} food items.")
    else:
        print("Food nutrient table already contains data, skipping seed.")
