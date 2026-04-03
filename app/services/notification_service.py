from fastapi_mail import MessageSchema, MessageType
from fastapi import BackgroundTasks
from loguru import logger
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, select
from app.models.notification_model import Notification
from app.models.semester_model import Semester
from app.models.student_model import Student
from app.models.user_model import User
from app.core import fastmail


class NotificationService:

    # send email
    @staticmethod
    async def send_single_email(
        to_email: str,
        subject: str,
        body: str
    ):
        message = MessageSchema(
            subject=subject,
            recipients=[to_email],  # type: ignore
            body=body,
            subtype=MessageType.html
        )

        await fastmail.send_message(message)
        logger.success(f"Email sent to {to_email}")

    @staticmethod
    async def send_bulk_emails(emails: list, subject: str, body: str):
        message = MessageSchema(
            subject=subject,
            recipients=emails,
            body=body,
            subtype=MessageType.html
        )
        await fastmail.send_message(message)
        logger.success(f"Email sent to {len(emails)} users")

    @staticmethod  # store single notification
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

        # return the email address to send email from the parent function as a background task
        user_stmt = select(User.email).where(User.id == user_id)
        email = (await db.execute(user_stmt)).scalar()

        await db.commit()
        return email

    @staticmethod  # store bulk notification
    async def store_bulk_publish_notification(
        db: AsyncSession,
        department_id: int,
        semester_id: int,
        session: str,
        background_tasks: BackgroundTasks
    ):
        # find semester name
        sem_stmt = select(Semester.semester_name).where(
            Semester.id == semester_id
        )
        sem_result = await db.execute(sem_stmt)
        semester_name = sem_result.scalars().one()

        # find all students of that semester+department+session with their email
        stmt = select(User.id, User.email)\
            .join(Student, Student.user_id == User.id)\
            .where(
            and_(
                Student.department_id == department_id,
                Student.session == session
            )
        )

        result = await db.execute(stmt)
        # will return [(id1, email1), (id2, email2)...]
        user_data = result.all()

        if not user_data:
            return

        title = "Result Published"
        text = f"Your result for {semester_name} semester has been published"

        # save notification in db
        notifications = [
            Notification(
                user_id=user.id,
                title="Result Published",
                message=text
            ) for user in user_data
        ]

        db.add_all(notifications)
        await db.commit()

        # create email lists
        email_list = [user.email for user in user_data]

        # background task for sending email
        background_tasks.add_task(
            NotificationService.send_bulk_emails,
            email_list,
            title,
            text
        )

    @staticmethod  # get last 5 notification
    async def get_latest_notification_for_a_user(db: AsyncSession, user_id: int):
        stmt = select(Notification).where(Notification.user_id == user_id).order_by(
            Notification.created_at.desc()).limit(5)
        notifications = await db.execute(stmt)
        return notifications.scalars().all()
