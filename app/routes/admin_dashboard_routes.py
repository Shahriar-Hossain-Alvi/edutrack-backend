from fastapi import APIRouter, Depends, HTTPException, status, Request
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import DomainIntegrityError
from app.db.db import get_db_session
from app.permissions import ensure_roles
from app.schemas.user_schema import UserOutSchema
from app.services.admin_dashboard_service import AdminDashboardService

router = APIRouter(
    prefix="/adminDashboard",
    tags=["admin dashboard"]  # for swagger
)


# get all tables data count for admin dashboard
@router.get("/allTableDataCount")
async def get_all_table_data_count_stats(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
    authorized_user: UserOutSchema = Depends(
        ensure_roles(["super_admin", "admin"])),
):
    try:
        return await AdminDashboardService.get_all_table_data_count(db, request)
    except DomainIntegrityError as de:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=de.error_message
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Unexpected Error: {e}")
        # attach audit payload
        if request:
            request.state.audit_payload = {
                "raw_error": str(e),
                "exception_type": type(e).__name__,
            }
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


# Department-wise Distribution: কোন ডিপার্টমেন্টে কতজন ছাত্র বা শিক্ষক আছে তার একটি Pie Chart।
@router.get("/pieChart")
async def get_chartsData(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
    authorized_user: UserOutSchema = Depends(
        ensure_roles(["super_admin", "admin"])),
):
    try:
        return await AdminDashboardService.get_chart_data(db, request)
    except DomainIntegrityError as de:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=de.error_message
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Unexpected Error: {e}")
        # attach audit payload
        if request:
            request.state.audit_payload = {
                "raw_error": str(e),
                "exception_type": type(e).__name__,
            }
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

# Result Performance: বিভিন্ন সেমিস্টারের গড় জিপিএ(Average GPA) এর একটি Bar Chart। এটি থেকে বোঝা যাবে কোন সেমিস্টারের রেজাল্ট কেমন হচ্ছে।

# 2. Audit Log Monitoring
# Showing Recent Activity: "Recent Activity" -> last 10 actions
# Filter by Level: শুধুমাত্র CRITICAL বা ERROR লেভেলের লগগুলো আলাদা করে দেখানোর জন্য একটি টগল বা বাটন।
# Database Load: আপনার অডিট টেবিল কত দ্রুত বড় হচ্ছে বা মোট কতগুলো এন্ট্রি আছে তার একটি স্ট্যাটাস।
