from typing import Any
from loguru import logger
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DomainIntegrityError
from app.core.integrity_error_parser import parse_integrity_error
from app.core.pw_hash import hash_password
from app.models.subject_offerings_model import SubjectOfferings
from app.models.user_model import User
from app.models.teacher_model import Teacher
from app.models.department_model import Department
from app.schemas.teacher_schema import TeacherCreateSchema, TeacherUpdateByAdminSchema
from app.utils import check_existence
from fastapi import HTTPException, Request, status
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import IntegrityError
from app.utils import delete_image_from_cloudinary
from app.utils.mask_sensitive_data import sanitize_payload


class TeacherService:

    @staticmethod  # create teacher
    async def create_teacher(
        teacher_data: TeacherCreateSchema,
        db: AsyncSession,
        request: Request | None = None
    ):
        # check for existance in user table
        existing_user = await db.scalar(select(User).where(User.username == teacher_data.user.username))

        if existing_user:
            logger.error("User with this email already exist")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with this email already exist")

        if not teacher_data.user.role.value == "teacher":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a teacher. Cannot create teacher.")

        # check if department exist
        if teacher_data.department_id:
            await check_existence(Department, db, teacher_data.department_id, "Department")

        try:
            # create user
            new_user_info = teacher_data.user.model_dump()
            raw_password = new_user_info.pop("password")

            new_user = User(
                **new_user_info,
                hashed_password=hash_password(raw_password)
            )

            db.add(new_user)
            await db.flush()  # This won't  add the user to the database yet but it'll generate a primary key for the user

            # create teacher
            new_teacher_info = teacher_data.model_dump(exclude={"user"})
            new_teacher = Teacher(
                **new_teacher_info,
                user_id=new_user.id
            )
            db.add(new_teacher)
            await db.commit()
            await db.refresh(new_teacher)
            logger.success("Teacher created successfully")

            return {
                "message": f"Teacher created successfully. Name: {new_teacher.name}, Teacher ID: {new_teacher.id}, User ID: {new_user.id}"
            }
        except IntegrityError as e:
            # Important: rollback as soon as an error occurs. It recovers the session from 'failed' state and puts it back in 'clean' state to save the Audit Log
            await db.rollback()

            # generally the PostgreSQL's error message will be in e.orig.args
            raw_error_message = str(e.orig) if e.orig else str(e)
            readable_error = parse_integrity_error(raw_error_message)

            logger.error(f"Integrity error while creating teacher: {e}")
            logger.error(readable_error)
            # attach audit payload safely
            if request:
                payload: dict[str, Any] = {
                    "raw_error": raw_error_message,
                    "readable_error": readable_error,
                }

                if teacher_data:
                    safe_data = sanitize_payload(
                        teacher_data.model_dump(
                            mode="json",
                            exclude={
                                "user": {
                                    "password",
                                    "hashed_password",
                                }
                            },
                        )
                    )
                    payload["data"] = safe_data

                request.state.audit_payload = payload

            raise DomainIntegrityError(
                error_message=readable_error, raw_error=raw_error_message
            )

    @staticmethod  # get single teacher
    async def get_teacher(db: AsyncSession, user_id: int):
        stmt = select(Teacher).where(Teacher.user_id == user_id).options(
            joinedload(Teacher.department),
            joinedload(Teacher.user)
        )

        teacher = await db.scalar(stmt)

        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")

        total_assigned_courses_stmt = select(func.count(SubjectOfferings.id)).where(
            SubjectOfferings.taught_by_id == teacher.id
        )
        total_assigned_courses = await db.scalar(total_assigned_courses_stmt)

        return {
            "user_data": teacher,
            "total_assigned_courses": total_assigned_courses
        }

    # Get all teacher with minimal data for course allocation (Subject Offering)

    @staticmethod
    async def get_all_teachers_with_minimal_data(
        db: AsyncSession,
        search: str | None = None,
        request: Request | None = None
    ):
        try:
            query = select(Teacher).options(
                selectinload(Teacher.department)
            ).order_by(Teacher.name)

            if search:
                query = query.where(
                    or_(
                        Teacher.name.ilike(f"%{search}%"),
                        Teacher.department.has(
                            Department.department_name.ilike(f"%{search}%"))
                    )
                )

            result = await db.execute(query)
            all_teachers = result.scalars().unique().all()

            return all_teachers

        except IntegrityError as e:
            # Important: rollback as soon as an error occurs. It recovers the session from 'failed' state and puts it back in 'clean' state to save the Audit Log
            await db.rollback()

            # generally the PostgreSQL's error message will be in e.orig.args
            raw_error_message = str(e.orig) if e.orig else str(e)
            readable_error = parse_integrity_error(raw_error_message)

            logger.error(
                f"Integrity error while fetching all teacher with minimal data: {e}")
            logger.error(f"Readable Error: {readable_error}")

            # attach audit payload safely
            if request:
                payload: dict[str, Any] = {
                    "raw_error": raw_error_message,
                    "readable_error": readable_error,
                }

                request.state.audit_payload = payload

            raise DomainIntegrityError(
                error_message=readable_error, raw_error=raw_error_message
            )

    @staticmethod
    async def update_teacher_by_admin(
        teacher_id: int,
        teacher_update_data: TeacherUpdateByAdminSchema,
        db: AsyncSession,
        request: Request | None = None,
    ):
        # check for teachers existence
        teacher = await check_existence(Teacher, db, teacher_id, "Teacher")
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")

        try:
            updated_teacher_data = teacher_update_data.model_dump(
                exclude_unset=True)

            if "photo_public_id" in updated_teacher_data:
                new_public_id = updated_teacher_data["photo_public_id"]
                old_public_id = teacher.photo_public_id

                if old_public_id and old_public_id != new_public_id:
                    await delete_image_from_cloudinary(old_public_id)
                    logger.success(
                        "Old teacher profile picture deleted from Cloudinary")

            for key, value in updated_teacher_data.items():
                setattr(teacher, key, value)

            await db.commit()
            await db.refresh(teacher)
            logger.success("Teacher updated successfully")

            return {
                "message": "Teacher updated successfully."
            }

        except IntegrityError as e:
            # Important: rollback as soon as an error occurs. It recovers the session from 'failed' state and puts it back in 'clean' state to save the Audit Log
            await db.rollback()

            # generally the PostgreSQL's error message will be in e.orig.args
            raw_error_message = str(e.orig) if e.orig else str(e)
            readable_error = parse_integrity_error(raw_error_message)

            logger.error(f"Integrity error while updating teacher(admin): {e}")
            logger.error(f"Readable Error: {readable_error}")

            # attach audit payload safely
            if request:
                payload: dict[str, Any] = {
                    "raw_error": raw_error_message,
                    "readable_error": readable_error,
                }

                if teacher_update_data:
                    payload["data"] = teacher_update_data.model_dump(
                        mode="json",
                        exclude_unset=True,
                    )

                request.state.audit_payload = payload

            raise DomainIntegrityError(
                error_message=readable_error, raw_error=raw_error_message
            )
