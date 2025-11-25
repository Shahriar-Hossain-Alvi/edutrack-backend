from sqlalchemy import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


async def check_existence(
        model,
        db: AsyncSession,
        model_id: int,
        model_name: str
):
    instance = await db.scalar(select(model).where(model.id == model_id))

    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{model_name} not found")

    return instance