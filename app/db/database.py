 
import pymongo
import motor.motor_asyncio

from core.config import DATABASE_URL

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client.get_database("college")
student_collection = db.get_collection("eiei-calories-tracker-db")

# helpers


def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }