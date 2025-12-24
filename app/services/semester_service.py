from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Semester
from app.schemas.semester_schema import SemesterCreateSchema, SemesterUpdateSchema
from sqlalchemy import select, or_


class SemesterService:

    @staticmethod
    async def create_semester(
        db: AsyncSession,
        semester_data: SemesterCreateSchema
    ):
        statement = select(Semester).where(
            or_(
                Semester.semester_name == semester_data.semester_name,
                Semester.semester_number == semester_data.semester_number
            )
        )
        result = await db.execute(statement)
        is_semester_exist = result.scalar_one_or_none()

        if (is_semester_exist):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Semester already exist")

        new_semester = Semester(**semester_data.model_dump())
        db.add(new_semester)
        await db.commit()
        await db.refresh(new_semester)

        return {
            "message": f"New Semester created successfully. ID: {new_semester.id}"
        }

    @staticmethod
    async def get_semesters(db: AsyncSession):
        statement = select(Semester).order_by(Semester.semester_number)
        result = await db.execute(statement)

        return result.scalars().all()

    @staticmethod
    async def get_semester(db: AsyncSession, semester_id: int):
        statement = select(Semester).where(Semester.id == semester_id)
        result = await db.execute(statement)

        return result.scalar_one_or_none()

    @staticmethod
    async def update_semester(
        db: AsyncSession,
        semester_id: int,
        semester_update_data: SemesterUpdateSchema
    ):
        statement = select(Semester).where(Semester.id == semester_id)
        result = await db.execute(statement)
        semester = result.scalar_one_or_none()

        if not semester:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Semester not found")

        updated_semester_data = semester_update_data.model_dump(
            exclude_unset=True)  # convert to dictionary

        for key, value in updated_semester_data.items():
            setattr(semester, key, value)

        await db.commit()
        await db.refresh(semester)

        return {
            "message": f"Semester updated successfully. ID: {semester.id}"
        }

    @staticmethod
    async def delete_semester(db: AsyncSession, semester_id: int):
        statement = select(Semester).where(Semester.id == semester_id)
        result = await db.execute(statement)
        semester = result.scalar_one_or_none()

        if not semester:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Semester not found")

        await db.delete(semester)
        await db.commit()

        return {"message": f"{semester.semester_name} semester deleted successfully"}
