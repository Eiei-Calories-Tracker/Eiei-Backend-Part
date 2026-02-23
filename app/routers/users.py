from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
 
from models.user import   ErrorResponseModel, ResponseModel,  StudentSchema
from services.user_service import add_student, retrieve_student 
 
 

router = APIRouter(prefix="/users", tags=["users"])

# @router.post("/heroes", response_model=Hero)
# def create_hero(hero: Hero, session: Session = Depends(get_session)):
#     session.add(hero)
#     session.commit()
#     session.refresh(hero)
#     return hero

@router.post("/", response_description="Student data added into the database")
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return ResponseModel(new_student, "Student added successfully.")

@router.get("/{id}", response_description="Student data retrieved")
async def get_student_data(id):
    student = await retrieve_student(id)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")