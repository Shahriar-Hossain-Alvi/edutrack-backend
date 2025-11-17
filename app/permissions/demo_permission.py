from sqlalchemy import select
from fastapi import Request, HTTPException, status, Depends
from functools import wraps
from typing import Callable, List, Type
from jose import JWTError
from app.core.jwt import decode_access_token
from app.db.db import AsyncSessionLocal, get_db_session
from app.models.user_model import User, UserRole


class BasePermission:
    def has_permission(self, user: User) -> bool:
        raise NotImplementedError


# Admin permissions
class IsAdmin(BasePermission):
    def has_permission(self, user: User) -> bool:
        return user.role == UserRole.ADMIN


class IsTeacher(BasePermission):
    def has_permission(self, user: User) -> bool:
        return user.role == UserRole.TEACHER
    
class IsStudent(BasePermission):
    def has_permission(self, user: User) -> bool:
        return user.role == UserRole.STUDENT


def permissions(required: List[Type[BasePermission]]): # outer function of decorator
    def decorator(func: Callable): # inner function of decorator
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs): 
            auth_header = request.headers.get("Authorization")
            print('auth heaer', auth_header)
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing or Invalid Token",
                )

            token = auth_header.replace("Bearer ", "")
            try:
                payload = decode_access_token(token)
                user_name = str(payload.get("sub"))
            except (JWTError, ValueError, TypeError) as e:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=str(e),
                    headers={"www-Authenticate": "Bearer"},
                )

            async with AsyncSessionLocal() as db:
                try:
                    stmt = select(User).where(User.username == user_name)
                    result = await db.execute(stmt)
                    user = result.scalar_one_or_none()
                    if not user:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found",
                        )

                    for perm in required:
                        if not perm().has_permission(user):
                            raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Permission Denied",
                            )

                    return await func(request, *args, **kwargs)
                finally:
                    await db.close()

        return wrapper

    return decorator
