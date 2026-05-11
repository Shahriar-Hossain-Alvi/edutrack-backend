from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log_model import AuditLog
from app.utils.paginator import Paginator


class AuditLogsService:

    @staticmethod
    # get audit log
    @staticmethod
    async def get_all_audit_logs(
        db: AsyncSession,
        page: int,
        size: int,
    ):
        query = select(AuditLog).order_by(
            AuditLog.created_at.desc())

        return await Paginator.paginate(db, query, page, size)
