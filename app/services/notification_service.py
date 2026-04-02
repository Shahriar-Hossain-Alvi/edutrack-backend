from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, select, update
from app.models.notification_model import Notification
from app.models.semester_model import Semester
from app.models.student_model import Student


class NotificationService:

    @staticmethod
    async def store_notification(
        db: AsyncSession,
        user_id: int,
        title: str,
        message: str
    ):
        new_notification = Notification(
            user_id=user_id,
            title=title,
            message=message
        )

        db.add(new_notification)
        await db.commit()

    @staticmethod
    async def store_bulk_publish_notification(
        db: AsyncSession,
        department_id: int,
        semester_id: int,
        session: str
    ):
        # find semester name
        sem_stmt = select(Semester.semester_name).where(
            Semester.id == semester_id
        )
        sem_result = await db.execute(sem_stmt)
        semester_name = sem_result.scalars().one()

        # find all students of that semester+department+session
        stmt = select(Student.user_id).where(
            and_(
                Student.department_id == department_id,
                Student.session == session
            )
        )

        result = await db.execute(stmt)
        user_ids = result.scalars().all()

        notifications = [
            Notification(
                user_id=uid,
                title="Result Published",
                message=f"Your result for {semester_name} semester have been published"
            ) for uid in user_ids
        ]

        db.add_all(notifications)
        await db.commit()
