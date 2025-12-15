from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_login_logout import login_user, logout_user
from app.db.db import get_db_session
from app.utils.token_injector import inject_token

# login router

router = APIRouter(prefix='/auth', tags=['login'])



# login route setup with httponly cookies
@router.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session)):
    try:
        return await login_user(db, form_data.username, form_data.password, response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/logout")
async def logout(
    response: Response,
    # token_injection: None = Depends(inject_token),
    ):
    try:
        return await logout_user(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))