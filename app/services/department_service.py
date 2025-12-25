from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.integrity_error_parser import parse_integrity_error
from app.models import Department
from app.schemas.department_schema import DepartmentCreateSchema, DepartmentOutSchema, DepartmentUpdateSchema
from sqlalchemy.exc import IntegrityError


class DepartmentService:

    @staticmethod
    async def create_department(
        db: AsyncSession,
        department_data: DepartmentCreateSchema
    ):
        lowercase_department_name = department_data.department_name.lower().strip()

        # check for existing department
        statement = select(Department).where(
            Department.department_name == lowercase_department_name)
        result = await db.execute(statement)
        is_exist = result.scalar_one_or_none()

        if (is_exist):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Department already exist")

        try:
            new_department = Department(
                department_name=lowercase_department_name)

            db.add(new_department)  # add the new_department to db(session)
            await db.commit()
            # refresh the object(get the new data)
            await db.refresh(new_department)

            return {
                "message": f"New Department created successfully. ID: {new_department.id}"
            }
        except IntegrityError as e:
            # generally the PostgreSQL's error message will be in e.orig.args[0]
            error_msg = str(e.orig.args[0]) if e.orig.args else str(  # type: ignore
                e)

            # send the error message to the parser
            readable_error = parse_integrity_error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=readable_error)

    @staticmethod
    async def get_departments(db: AsyncSession):
        statement = select(Department).order_by(Department.department_name)
        result = await db.execute(statement)

        return result.scalars().all()

    @staticmethod
    async def get_department(db: AsyncSession, department_id: int):
        statement = select(Department).where(Department.id == department_id)
        result = await db.execute(statement)

        return result.scalar_one_or_none()

    @staticmethod
    async def update_department(
        db: AsyncSession,
        department_id: int,
        department_data: DepartmentUpdateSchema
    ):
        statement = select(Department).where(Department.id == department_id)
        result = await db.execute(statement)
        department = result.scalar_one_or_none()

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

        try:
            lowercase_department_name = department_data.department_name.lower().strip()

            department.department_name = lowercase_department_name

            await db.commit()
            await db.refresh(department)

            return {
                "message": f"{department.department_name} department updated successfully. ID: {department.id}"
            }
        except IntegrityError as e:
            # generally the PostgreSQL's error message will be in e.orig.args[0]
            error_msg = str(e.orig.args[0]) if e.orig.args else str(  # type: ignore
                e)

            # send the error message to the parser
            readable_error = parse_integrity_error(error_msg)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=readable_error)

    @staticmethod
    async def delete_department(
        db: AsyncSession,
        department_id: int
    ):

        statement = select(Department).where(Department.id == department_id)
        result = await db.execute(statement)
        department = result.scalar_one_or_none()

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")

        await db.delete(department)
        await db.commit()

        return {"message": f"{department.department_name} department deleted successfully"}
