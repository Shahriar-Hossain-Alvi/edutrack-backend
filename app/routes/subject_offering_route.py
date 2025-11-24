from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.authenticated_user import get_current_user
from app.db.db import get_db_session
from app.permissions.role_checks import ensure_admin
from app.schemas.subject_offering_schema import SubjectOfferingCreateSchema, SubjectOfferingResponseSchema, SubjectOfferingUpdateSchema
from app.schemas.user_schema import UserOutSchema
from app.services.subject_offering_service import SubjectOfferingService


router = APIRouter(
    prefix="/subject_offering",
    tags=["subject_offering"] # for swagger
)

@router.post("/", dependencies=[Depends(ensure_admin)])
async def create_new_subject_offering(
    sub_off_data: SubjectOfferingCreateSchema,
    db: AsyncSession = Depends(get_db_session),
):
    
    return await SubjectOfferingService.create_subject_offering(sub_off_data, db)


@router.get("/{subject_offering_id}", response_model=SubjectOfferingResponseSchema)
async def get_single_subject_offering(
    subject_offering_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    return await SubjectOfferingService.get_subject_offering(db, subject_offering_id)


@router.get("/", response_model=list[SubjectOfferingResponseSchema])
async def get_all_subject_offerings(db: AsyncSession = Depends(get_db_session)):
    return await SubjectOfferingService.get_subject_offerings(db)


@router.patch("/{subject_offering_id}", response_model=SubjectOfferingResponseSchema,
dependencies=[Depends(ensure_admin)])
async def update_a_subject_offering(
    subject_offering_id: int,
    update_data: SubjectOfferingUpdateSchema,
    db: AsyncSession = Depends(get_db_session)
):  
    return await SubjectOfferingService.update_subject_offering(db, update_data, subject_offering_id)


@router.delete("/{subject_offering_id}", dependencies=[Depends(ensure_admin)])
async def delete_a_subject_offering(
    subject_offering_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    return await SubjectOfferingService.delete_subject_offering(db, subject_offering_id)