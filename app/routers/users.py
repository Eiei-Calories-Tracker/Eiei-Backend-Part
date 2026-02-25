from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from models.user import ErrorResponseModel, ResponseModel, StudentCreate, StudentUpdate, StudentRead
from services import user_service
from db.database import get_session

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(
    student: StudentCreate = Body(...),
    session: Session = Depends(get_session)
):
    """Add a new student to the database"""
    new_student = user_service.add_student(session, student)
    return new_student


@router.get("/", response_model=List[StudentRead])
def get_all_students(session: Session = Depends(get_session)):
    """Retrieve all students from the database"""
    students = user_service.retrieve_students(session)
    return students


@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: int, session: Session = Depends(get_session)):
    """Retrieve a student by ID"""
    student = user_service.retrieve_student(session, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student


@router.patch("/{student_id}", response_model=StudentRead)
def update_student(
    student_id: int,
    student_update: StudentUpdate,
    session: Session = Depends(get_session)
):
    """Update a student by ID"""
    updated_student = user_service.update_student(session, student_id, student_update)
    if not updated_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return updated_student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, session: Session = Depends(get_session)):
    """Delete a student by ID"""
    success = user_service.delete_student(session, student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return None