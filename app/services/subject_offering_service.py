from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.department_model import Department
from app.models.subject_model import Subject
from app.models.subject_offerings_model import SubjectOfferings
from app.models.user_model import User
from app.schemas.subject_offering_schema import SubjectOfferingCreateSchema, SubjectOfferingUpdateSchema
from fastapi import HTTPException, status
from app.utils import check_existence


class SubjectOfferingService:

    # create subject offering
    @staticmethod
    async def create_subject_offering(
        sub_off_data: SubjectOfferingCreateSchema,
        db: AsyncSession
    ):
        # validate teacher id and role
        teacher = await db.scalar(select(User).where(User.id == sub_off_data.taught_by_id))

        if not teacher or teacher.role.value != "teacher":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Teacher not found or not a teacher")

        # validate department id
        department = await db.scalar(select(Department).where(Department.id == sub_off_data.department_id))

        if not department:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

        # validate subject id
        subject = await db.scalar(select(Subject).where(Subject.id == sub_off_data.subject_id))

        if not subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")
        
        offered_subject = SubjectOfferings(
            **sub_off_data.model_dump()
        )

        db.add(offered_subject)
        await db.commit()
        await db.refresh(offered_subject)

        return {
            "message": f"Subject offering created successfully. ID: {offered_subject.id}"
        }


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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject offering not found")
        

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


        db.add(subject_offering)
        await db.commit()
        await db.refresh(subject_offering)

        return subject_offering
    

    @staticmethod
    async def delete_subject_offering(db: AsyncSession, subject_offering_id: int):
        subject_offering = await db.scalar(select(SubjectOfferings).where(SubjectOfferings.id == subject_offering_id))

        if not subject_offering:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject offering not found")
        
        await db.delete(subject_offering)
        await db.commit()

        return {
            "message": f"Subject offering deleted successfully. ID: {subject_offering.id}"
        }