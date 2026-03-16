from fastapi import FastAPI
from core.config import PORT
from routers import users
from routers.v1 import auth as auth_v1
from routers.v1 import users as users_v1
from routers.v1 import food as food_v1
from routers.v1 import nutrition as nutrition_v1
from db.database import create_db_and_tables
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ตอน dev ใช้ * ไปก่อน
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Initialize database tables and seed data on startup"""
    create_db_and_tables()
    
    # Seed food data
    from db.database import SessionLocal
    from db.seed import seed_food_nutrients
    with SessionLocal() as session:
        seed_food_nutrients(session)


app.include_router(users.router)
app.include_router(auth_v1.router, prefix="/api/v1")
app.include_router(users_v1.router, prefix="/api/v1")
app.include_router(food_v1.router, prefix="/api/v1")
app.include_router(nutrition_v1.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)