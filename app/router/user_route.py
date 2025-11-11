from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud_operations.user_service import create_user, get_users
from app.db.db import get_db_session
from app.schemas.user_schema import UserCreateSchema


router = APIRouter(
    prefix="/users", # eg: /users/register, /users/:id
    tags=["users"] # for swagger
)


# user register
@router.post("/register")
async def register_user(user_data: UserCreateSchema ,db: AsyncSession = Depends(get_db_session)):
    try:
        new_user = await create_user(db, user_data)

        return {"message": f"User created successfully. ID: {new_user.id}"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/", response_model=list[UserCreateSchema])
async def get_all_users(db: AsyncSession = Depends(get_db_session)):
    try:
        users = await get_users(db)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))