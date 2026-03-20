from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session
from datetime import datetime
from services import food_record_service
from models.record import FoodRecord
import os
from services import s3_service
router = APIRouter(prefix='', tags=["foodrecord"])
BUCKET_S3 = os.getenv("AWS_STORAGE_BUCKET_NAME")

@router.get("/foodrecord/{user_id}/{date}")
async def get_food_record(
    user_id: int,
    date: datetime,
    session: Session=Depends(get_session),
    
) -> list[FoodRecord]:
    foodRecord : list[FoodRecord] = food_record_service.get_food_records_by_date(session, user_id, date)
    for i in range(len(foodRecord)):
        foodRecord[i].image_key = s3_service.generate_presigned_url(foodRecord[i].image_key)
    return foodRecord
