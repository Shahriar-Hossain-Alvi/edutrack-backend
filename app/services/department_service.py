from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Department
from app.schemas.department_schema import  DepartmentCreateSchema, DepartmentOutSchema, DepartmentUpdateSchema

# TODO: create Department Service class

async def create_department(
        db: AsyncSession, 
        department_data: DepartmentCreateSchema
    ):
    lowercase_department_name = department_data.department_name.lower().strip()

    # check for existing department
    statement = select(Department).where(Department.department_name == lowercase_department_name)
    result = await db.execute(statement)
    is_exist = result.scalar_one_or_none()

    if(is_exist):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Department already exist")

    new_department = Department(department_name=lowercase_department_name)
    
    db.add(new_department)  # add the new_department to db(session)
    await db.commit()
    await db.refresh(new_department) # refresh the object(get the new data)

    return {
        "message": f"new_department created successfully. ID: {new_department.id}"
    }

async def get_departments(db: AsyncSession):
    statement = select(Department)
    result = await db.execute(statement)

    return result.scalars().all()


async def get_department(db: AsyncSession, department_id: int):
    statement = select(Department).where(Department.id == department_id)
    result = await db.execute(statement)

    return result.scalar_one_or_none()


async def update_department(
    db: AsyncSession, 
    department_id: int,
    department_data: DepartmentUpdateSchema
    ):
    statement = select(Department).where(Department.id == department_id)
    result = await db.execute(statement)
    department = result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

    lowercase_department_name = department_data.department_name.lower().strip()

    department.department_name = lowercase_department_name

    await db.commit()
    await db.refresh(department)

    return department

async def delete_department(
    db: AsyncSession,
    department_id: int
    ):
    
    statement = select(Department).where(Department.id == department_id)
    result = await db.execute(statement)
    department = result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    
    await db.delete(department)
    await db.commit()

    return {"message": f"{department.department_name} department deleted successfully"}