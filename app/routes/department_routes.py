from fastapi import APIRouter, Depends, HTTPException
from app.core.authenticated_user import get_current_user
from app.crud_operations.department_service import create_department, delete_department, get_department, get_departments, update_department
from app.models.user_model import UserRole
from app.schemas.department_schema import DepartmentCreateSchema, DepartmentOutSchema, DepartmentUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_db_session
from app.schemas.user_schema import UserOutSchema


router = APIRouter(
    prefix="/departments",
    tags=["departments"] # for swagger
)


# create department
@router.post("/")
async def create_new_department(
    department_data: DepartmentCreateSchema, 
    db: AsyncSession = Depends(get_db_session),
    current_user: UserOutSchema = Depends(get_current_user)
    ):
    # if current_user.role != UserRole.ADMIN:
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create a new department")
    print("DEPARTMENT DATA", department_data)
    try:
       return await create_department(db, department_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all departments     
@router.get("/", response_model=list[DepartmentOutSchema])
async def get_all_departments(
    db: AsyncSession = Depends(get_db_session),
    current_user: UserOutSchema = Depends(get_current_user)
    ):

    try: 
        return await get_departments(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# get single department
@router.get("/{id}", response_model=DepartmentOutSchema)
async def get_single_department(
    id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserOutSchema = Depends(get_current_user)
    ):

    try:
        return await get_department(db, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# update a department
@router.patch("/{id}", response_model=DepartmentOutSchema)
async def update_single_department(
    id: int,
    department_data: DepartmentUpdateSchema,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserOutSchema = Depends(get_current_user)
    ):

    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized access")

    try:
        return await update_department(db, id, department_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
# delete a department
@router.delete("/{id}")
async def delete_single_department(
    id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserOutSchema = Depends(get_current_user)
):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized access")

    try:
        return await delete_department(db, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))