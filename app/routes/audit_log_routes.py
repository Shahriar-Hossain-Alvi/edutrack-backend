from fastapi import APIRouter
from app.schemas.admin_dashboard_schema import AuditLogsResponseSchema
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db_session
from app.permissions import ensure_roles
from app.schemas.admin_dashboard_schema import AuditLogsResponseSchema
from app.schemas.pagination_schema import PaginatedResponse
from app.schemas.user_schema import UserOutSchema
from app.services.audit_logs_service import AuditLogsService


router = APIRouter(
    prefix="/auditLogs",
    tags=["audit logs"]  # for swagger
)


# get all audit logs
@router.get("/", response_model=PaginatedResponse[AuditLogsResponseSchema])
async def get_audit_logs(
    page: int = 1,
    size: int = 10,
    filter_by_level: str | None = None,
    db: AsyncSession = Depends(get_db_session),
    authorized_user: UserOutSchema = Depends(
        ensure_roles(["super_admin", "admin"])),
):
    try:
        return await AuditLogsService.get_all_audit_logs(db, page, size, filter_by_level)
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Unexpected Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
