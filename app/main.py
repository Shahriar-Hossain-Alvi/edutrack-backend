from fastapi import FastAPI
import uvicorn


app = FastAPI()

# install asyncpg



if __name__ == "__main__":
    # asyncio.run(init_db())
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)