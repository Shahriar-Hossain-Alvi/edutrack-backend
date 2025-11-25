from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.department_model import Department
from app.models.semester_model import Semester
from app.models.student_model import Student
from app.models.user_model import User
from app.schemas.student_schema import StudentCreateSchema, StudentUpdateSchema
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload, selectinload


# TODO: create Student Service class

class StudentService:

    @staticmethod
    async def create_student(
            db: AsyncSession,
            student_data: StudentCreateSchema
    ):
        # check for existing user
        user = await db.scalar(select(User).where(User.id == student_data.user_id))

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found. Cannot create student")

        if not user.role.value == "student":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a student. Cannot create student")

        # check for existing student
        student = await db.scalar(select(Student).where(Student.user_id == student_data.user_id))

        if (student):
            raise ValueError("Student already exist")

        # check if department exist
        department = await db.scalar(select(Department).where(Department.id == student_data.department_id))

        if not department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Department not found. Student cannot be created")

        # check if semester exist
        semester = await db.scalar(select(Semester).where(Semester.id == student_data.semester_id))

        if not semester:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Semester not found. Student cannot be created")

        new_student = Student(**student_data.model_dump())
        db.add(new_student)
        await db.commit()
        await db.refresh(new_student)

        return {
            "message": f"new_student created successfully. ID: {new_student.id}"
        }

    @staticmethod
    async def get_students(
            db: AsyncSession
    ):
        students = await db.scalars(select(Student))

        return students.all()

    @staticmethod
    async def get_student(
            db: AsyncSession,
            student_id: int
    ):

        stmt = select(Student).where(Student.id == student_id).options(
                joinedload(Student.user) # Eager load user
            )

        student = await db.scalar(stmt)

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        return student

    @staticmethod
    async def update_student(
            db: AsyncSession,
            student_id: int,
            student_update_data: StudentUpdateSchema
    ):
        # check for existing student
        student = await db.scalar(select(Student).where(Student.id == student_id))

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        updated_student_data = student_update_data.model_dump(
            exclude_unset=True)  # convert to dictionary

        for key, value in updated_student_data.items():
            # apply the updated data in the student object(from DB)
            setattr(student, key, value)

        await db.commit()
        await db.refresh(student)

        return student

    @staticmethod
    async def delete_student(
            db: AsyncSession,
            student_id: int
    ):
        student = await StudentService.get_student(db, student_id)

        await db.delete(student)
        await db.commit()

        return {"message": f"{student.name} student deleted successfully"}
