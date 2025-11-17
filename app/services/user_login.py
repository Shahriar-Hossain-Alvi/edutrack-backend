from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import verify_password, create_access_token
from app.models import User

async def login_user(
        db: AsyncSession,
        username: str,
        password: str
    ):
    # get user
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if not user: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    
    # verify password
    is_valid = verify_password(password, user.hashed_password)

    if not is_valid:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials")
    
    # after validating the user, create access token
    access_token = create_access_token(user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    } # this token will be stored in the frontend and will be sent to backend for authentication with protected routes