from app.schemas.marks_schema import MarksCreateSchema, MarksResponseSchema, MarksUpdateSchema
from app.schemas.user_schema import UserOutSchema
from app.services.marks_service import MarksService
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db_session
from app.permissions.role_checks import ensure_admin_or_teacher, ensure_admin
from app.core.authenticated_user import get_current_user


router = APIRouter(
    prefix="/marks",
    tags=["marks"] # for swagger
)


# create marks
@router.post("/", 
    dependencies=[Depends(ensure_admin_or_teacher)],
    response_model=MarksResponseSchema
)
async def create_new_mark(
    mark_data: MarksCreateSchema,
    current_user: UserOutSchema = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    
    return await MarksService.create_mark(db, mark_data, current_user)


# update marks
@router.patch("/{mark_id}",
    dependencies=[Depends(ensure_admin_or_teacher)],
    response_model=MarksResponseSchema              
)
async def update_a_mark(
    mark_id: int,
    mark_data: MarksUpdateSchema,
    current_user: UserOutSchema = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):

    return await MarksService.update_mark(db, mark_data, mark_id, current_user)


# delete marks
@router.delete("/{mark_id}",
    dependencies=[Depends(ensure_admin)],
    response_model=MarksResponseSchema
)
async def delete_a_mark(
    mark_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    return await MarksService.delete_mark(db, mark_id)


# get all subjects marks for a student
@router.get("/student/{student_id}",)
async def get_all_subjects_marks_for_a_student(
    student_id: int,
    semester_id: int | None = Query(None),
    subject_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db_session),
    current_user: UserOutSchema = Depends(get_current_user),
):
    return await MarksService.get_all_marks_for_a_student(db, student_id, semester_id, subject_id)