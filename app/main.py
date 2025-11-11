# this project is using python 3.12 interpreter
from fastapi import FastAPI
import uvicorn

from app.router import user_route

app = FastAPI()


# add the routes
app.include_router(user_route.router, prefix="/api")


if __name__ == "__main__":
    # asyncio.run(init_db())
    uvicorn.run(app, host="0.0.0.0", port=8000)
