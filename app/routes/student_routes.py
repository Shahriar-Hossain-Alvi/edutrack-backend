from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.authenticated_user import get_current_user
from app.services.student_service import create_student, delete_student, get_student, get_students, update_student
from app.db.db import get_db_session
from app.permissions.role_checks import ensure_admin_or_teacher, ensure_admin
from app.schemas.student_schema import StudentCreateSchema, StudentOutSchema, StudentUpdateSchema
from app.schemas.user_schema import UserOutSchema

router = APIRouter(
    prefix="/students",
    tags=["students"]  # for swagger
)


# create student record
@router.post("/", dependencies=[Depends(ensure_admin)])
async def create_student_record(
        student_data: StudentCreateSchema,
        db: AsyncSession = Depends(get_db_session),
):

    try:
        return await create_student(db, student_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# get all students
@router.get(
    "/",
    response_model=list[StudentOutSchema],
    dependencies=[Depends(ensure_admin_or_teacher)]
)
async def get_all_students(
    db: AsyncSession = Depends(get_db_session),
):

    try:
        return await get_students(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# get single student
@router.get("/{id}", response_model=StudentOutSchema)
async def get_single_student(
    id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserOutSchema = Depends(get_current_user),
):
    try:
        return await get_student(db, id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# update a student
@router.patch("/{id}",
              response_model=StudentOutSchema,
              dependencies=[Depends(ensure_admin)]
              )
async def update_single_student(
    id: int,
    student_data: StudentUpdateSchema,
    db: AsyncSession = Depends(get_db_session),
):

    try:
        return await update_student(db, id, student_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# delete a student
@router.delete("/{id}", dependencies=[Depends(ensure_admin)])
async def delete_single_student(
    id: int,
    db: AsyncSession = Depends(get_db_session),
):

    try:
        return await delete_student(db, id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
