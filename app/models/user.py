from typing import Optional
from sqlmodel import SQLModel, Field


class StudentBase(SQLModel):
    fullname: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    course_of_study: str
    year: int = Field(gt=0, lt=9)
    gpa: float = Field(le=4.0, ge=0.0)


class Student(StudentBase, table=True):
    """Student table model"""
    id: Optional[int] = Field(default=None, primary_key=True)


class StudentCreate(StudentBase):
    """Schema for creating a student"""
    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources engineering",
                "year": 2,
                "gpa": 3.0,
            }
        }


class StudentUpdate(SQLModel):
    """Schema for updating a student"""
    fullname: Optional[str] = None
    email: Optional[str] = None
    course_of_study: Optional[str] = None
    year: Optional[int] = Field(default=None, gt=0, lt=9)
    gpa: Optional[float] = Field(default=None, le=4.0, ge=0.0)

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources and environmental engineering",
                "year": 4,
                "gpa": 4.0,
            }
        }


class StudentRead(StudentBase):
    """Schema for reading a student"""
    id: int


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}