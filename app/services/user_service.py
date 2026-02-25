from sqlmodel import Session, select
from models.user import Student, StudentCreate, StudentUpdate
from typing import List, Optional


def retrieve_students(session: Session) -> List[Student]:
    """Retrieve all students from the database"""
    statement = select(Student)
    students = session.exec(statement).all()
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
    print("get",student)
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