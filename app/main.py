from fastapi import FastAPI # type: ignore
from app.config.database import db
from app.config.redis_client import redis_client
from app.routes.auth import router as auth_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Auth Service", version="1.0.0")
app.include_router(auth_router, prefix="/auth")

@app.on_event("startup")
async def startup():
    await db.connect()
    try:
        redis_client.ping()
        logger.info("Connected to Redis")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
    logger.info("Auth Service started")

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    redis_client.close()
    logger.info("Auth Service shutdown")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)