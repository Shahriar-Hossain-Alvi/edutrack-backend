from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import math


class Paginator:
    @staticmethod
    async def paginate(
        db: AsyncSession,
        query,  # sqlalchemy query
        page: int = 1,
        size: int = 10,
    ):
        # count total items
        count_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_query)).scalar() or 0

        # calculate page limit
        offset = (page - 1) * size
        pages = math.ceil(total / size) if total > 0 else 0

        # execute main query
        paginated_query = query.offset(offset).limit(size)
        result = await db.execute(paginated_query)
        items = result.scalars().all()

        return {
            "total": total,
            "page": page,
            "size": size,
            "pages": pages,
            "items": items
        }
