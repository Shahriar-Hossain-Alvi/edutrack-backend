from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select
from app.core.integrity_error_parser import parse_integrity_error
from app.models.subject_model import Subject
from app.models.subject_offerings_model import SubjectOfferings
from app.schemas.subject_schema import SubjectCreateSchema
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.schemas.user_schema import UserOutSchema


class SubjectService:

    @staticmethod
    async def create_subject(
            db: AsyncSession,
            subject_data: SubjectCreateSchema
    ):
        capitalized_subject_code = subject_data.subject_code.upper().strip()

        # check for existing subject
        subject = await db.scalar(select(Subject).where(Subject.subject_code == capitalized_subject_code))

        if subject:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Subject already exist")

        try:
            new_subject = Subject(
                **subject_data.model_dump(exclude={"subject_code"}), subject_code=capitalized_subject_code)

            db.add(new_subject)
            await db.commit()
            await db.refresh(new_subject)

            return {
                "message": f"new_subject created successfully. ID: {new_subject.id}"
            }
        except IntegrityError as e:
            # generally the PostgreSQL's error message will be in e.orig.args[0]
            error_msg = str(e.orig.args[0]) if e.orig.args else str(  # type: ignore
                e)

            # send the error message to the parser
            readable_error = parse_integrity_error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=readable_error)

    @staticmethod
    async def get_subject(db: AsyncSession, subject_id: int):
        subject = await db.scalar(select(Subject).where(Subject.id == subject_id))

        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

        return subject

    @staticmethod
    async def get_subjects(db: AsyncSession):
        subjects = await db.execute(select(Subject))

        return subjects.scalars().all()

    @staticmethod
    async def delete_subject(
        db: AsyncSession,
        subject_id: int
    ):
        subject = await db.scalar(select(Subject).where(Subject.id == subject_id))

        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

        await db.delete(subject)
        await db.commit()

        return {"message": f"{subject.subject_title} subject deleted successfully"}

    @staticmethod
    async def get_subject_by_code(
            db: AsyncSession,
            subject_code: str
    ):
        capitalized_subject_code = subject_code.upper().strip()

        subject = await db.scalar(select(Subject).where(Subject.subject_code == capitalized_subject_code))

        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

        return subject
