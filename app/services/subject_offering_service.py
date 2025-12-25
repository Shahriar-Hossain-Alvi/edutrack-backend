from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.integrity_error_parser import parse_integrity_error
from app.models.department_model import Department
from app.models.subject_model import Subject
from app.models.subject_offerings_model import SubjectOfferings
from app.models.user_model import User
from app.schemas.subject_offering_schema import SubjectOfferingCreateSchema, SubjectOfferingUpdateSchema
from fastapi import HTTPException, status
from app.schemas.user_schema import UserOutSchema
from app.utils import check_existence
from sqlalchemy.exc import IntegrityError


class SubjectOfferingService:

    # create subject offering
    @staticmethod
    async def create_subject_offering(
        sub_off_data: SubjectOfferingCreateSchema,
        db: AsyncSession
    ):
        # validate teacher id and role
        teacher = await check_existence(User, db, sub_off_data.taught_by_id, "Teacher")

        # teacher = await db.scalar(select(User).where(User.id == sub_off_data.taught_by_id))

        if teacher.role.value != "teacher":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not a teacher")

        # validate department id
        await check_existence(Department, db, sub_off_data.department_id, "Department")

        # department = await db.scalar(select(Department).where(Department.id == sub_off_data.department_id))

        # if not department:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

        # validate subject id
        await check_existence(Subject, db, sub_off_data.subject_id, "Subject")

        # subject = await db.scalar(select(Subject).where(Subject.id == sub_off_data.subject_id))

        # if not subject:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

        try:
            offered_subject = SubjectOfferings(
                **sub_off_data.model_dump()
            )

            db.add(offered_subject)
            await db.commit()
            await db.refresh(offered_subject)

            return {
                "message": f"Subject offering created successfully. ID: {offered_subject.id}"
            }
        except IntegrityError as e:
            # generally the PostgreSQL's error message will be in e.orig.args[0]
            error_msg = str(e.orig.args[0]) if e.orig.args else str(  # type: ignore
                e)

            # send the error message to the parser
            readable_error = parse_integrity_error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=readable_error)

    # get single subject offering

    @staticmethod
    async def get_subject_offering(db: AsyncSession, subject_offering_id: int):
        subject_offering = await db.scalar(select(SubjectOfferings).where(SubjectOfferings.id == subject_offering_id))

        if not subject_offering:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Subject offering not found")

        return subject_offering

    # get all subject offerings

    @staticmethod
    async def get_subject_offerings(db: AsyncSession):
        subject_offerings = await db.scalars(select(SubjectOfferings))

        return subject_offerings.all()

    # update subject offering

    @staticmethod
    async def update_subject_offering(db: AsyncSession, update_data: SubjectOfferingUpdateSchema, subject_offering_id: int):

        # check for existing subject offering
        subject_offering = await db.scalar(select(SubjectOfferings).where(SubjectOfferings.id == subject_offering_id))

        if not subject_offering:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Subject offering not found")

        updated_data = update_data.model_dump(exclude_unset=True)

        # check if taught_by exists
        if "taught_by_id" in updated_data:
            await check_existence(User, db, updated_data["taught_by_id"], "Teacher")

        # check if department exists
        if "department_id" in updated_data:
            await check_existence(Department, db, updated_data["department_id"], "Department")

        # check if subject exists
        if "subject_id" in updated_data:
            await check_existence(Subject, db, updated_data["subject_id"], "Subject")

        for key, value in updated_data.items():
            setattr(subject_offering, key, value)

        try:
            db.add(subject_offering)
            await db.commit()
            await db.refresh(subject_offering)

            return subject_offering
        except IntegrityError as e:
            # generally the PostgreSQL's error message will be in e.orig.args[0]
            error_msg = str(e.orig.args[0]) if e.orig.args else str(  # type: ignore
                e)

            # send the error message to the parser
            readable_error = parse_integrity_error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=readable_error)

    @staticmethod
    async def delete_subject_offering(db: AsyncSession, subject_offering_id: int):
        subject_offering = await db.scalar(select(SubjectOfferings).where(SubjectOfferings.id == subject_offering_id))

        if not subject_offering:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Subject offering not found")

        await db.delete(subject_offering)
        await db.commit()

        return {
            "message": f"Subject offering deleted successfully. ID: {subject_offering.id}"
        }

    # get offered subjects for marking
    # admin -> see all subjects for marking
    # teacher -> see only the subjects they teach

    @staticmethod
    async def get_offered_subjects_for_marking(
        db: AsyncSession,
        semester_id: int,
        department_id: int,
        current_user: UserOutSchema
    ):
        stmt = select(Subject)\
            .join(Subject.subject_offerings)\
            .where(
                and_(
                    Subject.semester_id == semester_id,
                    SubjectOfferings.department_id == department_id
                )
        )

        # restrict subject list for teachers
        if current_user.role.value == "teacher":
            stmt = stmt.where(
                SubjectOfferings.taught_by_id == current_user.id
            )

        result = await db.execute(stmt)
        subjects = result.scalars().all()
        return subjects
