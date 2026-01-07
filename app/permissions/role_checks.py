from fastapi import HTTPException, Depends
from app.core.authenticated_user import get_current_user
from app.schemas.user_schema import UserOutSchema

# This functions already returns the current user, so passing current_user as get_current_user dependency will be redundant wherever this function is used

# ensure super admin


def ensure_super_admin(current_user: UserOutSchema = Depends(get_current_user)):
    if current_user.role.value != "super_admin":
        raise HTTPException(status_code=403, detail="Unauthorized access")
    return current_user

# ensure admin


def ensure_admin(current_user: UserOutSchema = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized access")
    return current_user

# ensure admin or teacher


def ensure_admin_or_teacher(current_user: UserOutSchema = Depends(get_current_user)):
    if current_user.role.value not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    return current_user

# ensure admin or teacher


def ensure_student(current_user: UserOutSchema = Depends(get_current_user)):
    if current_user.role.value != "student":
        raise HTTPException(status_code=403, detail="Unauthorized access")
    return current_user


"""
from fastapi import HTTPException, status, Depends
from typing import List

def ensure_roles(allowed_roles: List[str]):

একইসাথে একাধিক রোলকে পারমিশন দেওয়ার জন্য ডিপেন্ডেন্সি।
ব্যবহার: Depends(ensure_roles(["super_admin", "admin", "teacher"]))

    async def role_checker(current_user: UserOutSchema = Depends(get_current_user)):
        # current_user.role.value বা আপনার মডেলের ফিল্ড নাম অনুযায়ী চেক করুন
        if current_user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}"
            )
        return current_user
    
    return role_checker
"""

# Use in router
"""
@router.get("/", response_model=list[AllUsersWithDetailsResponseSchema])
async def get_all_users(
    user_role: str | None = None,
    db: AsyncSession = Depends(get_db_session),
    # এখানে আমরা লিস্ট আকারে রোলগুলো বলে দিচ্ছি
    authorized_user: UserOutSchema = Depends(
        ensure_roles(["super_admin", "admin", "teacher"])
    )
):
    # কোড লজিক...
    return await UserService.get_all_users(db, user_role)
"""
