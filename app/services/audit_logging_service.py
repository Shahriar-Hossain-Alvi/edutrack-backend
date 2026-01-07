from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.integrity_error_parser import parse_integrity_error
from app.db.db import AsyncSessionLocal
from app.models.audit_log_model import AuditLog, LogLevel
from sqlalchemy.exc import IntegrityError
from loguru import logger


async def create_audit_log_isolated(
    action: str,  # CREATE USER / UPDATE USER / DELETE USER
    request: Request | None = None,
    level: str = "info",  # info for success, error for error
    details: str | None = None,  # custom message
    # user id (who sent the request eg; ID from get_current_user or authoried user)
    created_by: int | None = None,
    payload: dict | None = None
):
    # Always Uses Fresh Session, Safe even the main session(Inside another transaction/service function) failed
    """
    Rules (MEMORIZE THESE)
    -> Never log with a failed session
    -> Audit Logs get their own session
    -> Logging must never raise
    -> One business request ≠ one logging transaction
    -> Rollback ≠ safe reuse
    """

    """
    Why rollback + same session still fails?
    Because:
    -- ORM state is partially invalid
    -- async greenlet context is broken
    -- SQLAlchemy explicitly warns against reuse
    """

    async with AsyncSessionLocal() as session:
        # No greenlet issue
        # No session reuse
        # Works after ANY error
        try:
            new_log = AuditLog(
                created_by=created_by,
                level=level,
                action=action,
                method=request.method if request else None,
                path=request.url.path if request else None,
                ip_address=request.client.host if request else None,  # type: ignore
                details=details,
                payload=payload or {},
            )

            session.add(new_log)
            await session.commit()
            logger.success("Adding Audit Log to DB")
        except Exception as e:
            # never raise just log
            await session.rollback()
            logger.critical(f"CRITICAL: Failed to save Audit Log: {e}")
