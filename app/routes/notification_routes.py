from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db_session
from app.schemas.notification_schema import NotificationResponseSchema
from app.services.notification_service import NotificationService
from app.core.authenticated_user import get_current_user
from app.schemas.user_schema import UserOutSchema


router = APIRouter(
    prefix="/notifications",  # eg: /users/, /users/:id
    tags=["notifications"]  # for swagger
)


# get latest notifications for a user
@router.get("/{id}", response_model=list[NotificationResponseSchema])
async def get_latest_notifications(
    id: int,
    current_user: UserOutSchema = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
):
    if current_user.id != id:
        raise HTTPException(
            status_code=400, detail="You are not authorized to view this record.")

    try:
        return await NotificationService.get_latest_notification_for_a_user(db, id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
