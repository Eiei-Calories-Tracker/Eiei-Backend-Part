from sqlmodel import select
from sqlalchemy.orm import Session
from models.user import Student, StudentCreate, StudentUpdate
from models.account import UserAccount, UserAccountUpdate
from typing import List, Optional

# --- Student Service (Legacy) ---
def retrieve_students(session: Session) -> List[Student]:
    """Retrieve all students from the database"""
    statement = select(Student)
    students = session.scalars(statement).all()
    return students

def add_student(session: Session, student_data: StudentCreate) -> Student:
    """Add a new student to the database"""
    student = Student.model_validate(student_data)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def retrieve_student(session: Session, student_id: int) -> Optional[Student]:
    """Retrieve a student with a matching ID"""
    student = session.get(Student, student_id)
    return student

def update_student(session: Session, student_id: int, student_data: StudentUpdate) -> Optional[Student]:
    """Update a student with a matching ID"""
    student = session.get(Student, student_id)
    if not student:
        return None
    
    # Update only provided fields
    student_dict = student_data.model_dump(exclude_unset=True)
    for key, value in student_dict.items():
        setattr(student, key, value)
    
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def delete_student(session: Session, student_id: int) -> bool:
    """Delete a student from the database"""
    student = session.get(Student, student_id)
    if not student:
        return False
    
    session.delete(student)
    session.commit()
    return True

# --- User Account Service (New) ---
def update_user_profile(session: Session, user: UserAccount, update_data: UserAccountUpdate) -> UserAccount:
    """Update user profile with provided partial data"""
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

