import httpx
from fastapi import UploadFile
from core.config import AI_PREDICT_URL

async def predict_food_from_image(file: UploadFile):
    """Send image to external AI service and return prediction results"""
    async with httpx.AsyncClient() as client:
        files = {"file": (file.filename, await file.read(), file.content_type)}
        response = await client.post(f'{AI_PREDICT_URL}/predict', files=files, timeout=30.0)
        
        if response.status_code != 200:
            return None
            
        return response.json()
