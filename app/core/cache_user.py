from typing import Any

from cachetools import TTLCache

from app.models.user_model import User

# store 100 users in cache for 10 minutes (600 seconds) then auto clear from memory
user_cache = TTLCache(maxsize=100, ttl=600)


class CacheService:
    @staticmethod
    def set_user(username: str, user_data: User):
        user_cache[username] = user_data

    @staticmethod
    def get_user(username: str) -> User | None:
        return user_cache.get(username)

    @staticmethod
    def clear_user(username: str):
        if username in user_cache:
            del user_cache[username]
