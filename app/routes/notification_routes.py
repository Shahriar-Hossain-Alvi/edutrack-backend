from fastapi import APIRouter, Depends, HTTPException, Request, WebSocket, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DomainIntegrityError
from app.db.db import get_db_session
from app.permissions.role_checks import ensure_roles
from app.schemas.notification_schema import NotificationResponseSchema
from app.services.notification_service import NotificationService
from app.core import get_current_user, manager
from app.schemas.user_schema import UserOutSchema


router = APIRouter(
    prefix="/notifications",  # eg: /users/, /users/:id
    tags=["notifications"]  # for swagger
)


# send notification through websocket
@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            # keep the connection alive
            data = await websocket.receive_text()
            logger.success("Websocket message received")
    except Exception:
        logger.critical("Websocket connection closed")
        manager.disconnect(user_id)


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


@router.patch("/{id}")
async def mark_notification_as_read(
    request: Request,
    id: int,
    update_data: dict,
    db: AsyncSession = Depends(get_db_session),
    authorized_user: UserOutSchema = Depends(
        ensure_roles(["student"])),
):
    # attach action
    request.state.action = "UPDATE NOTIFICATION READ STATUS BY SELF"

    try:
        return await NotificationService.mark_notification_as_read(db, id, update_data, request)
    except DomainIntegrityError as de:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=de.error_message
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Notification update unexpected error: {e}")

        # attach audit payload
        if request:
            request.state.audit_payload = {
                "raw_error": str(e),
                "exception_type": type(e).__name__,
            }
        raise HTTPException(status_code=500, detail="Internal Server Error")
