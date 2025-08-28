from app.config.database import db
from app.models.user import UserInDB
from app.utils.password import get_password_hash, verify_password
from app.utils.jwt import create_jwt_token
from app.config.redis_client import redis_client
from app.config.env import ENV
from datetime import datetime, timedelta
from bson import ObjectId # type: ignore

async def get_user_by_username(username: str):
    return await db.users.find_one({"username": username})

async def get_user_by_email(email: str):
    return await db.users.find_one({"email": email})

async def register_user(username: str, email: str, password: str):
    if await get_user_by_username(username) or await get_user_by_email(email):
        return None
    
    hashed_password = get_password_hash(password)
    
    user_doc = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    
    return UserInDB(
        id=str(result.inserted_id),
        username=username,
        email=email,
        hashed_password=hashed_password,
        created_at=user_doc["created_at"],
        updated_at=user_doc["updated_at"]
    )

async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    
    return UserInDB(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"],
        hashed_password=user["hashed_password"],
        created_at=user.get("created_at"),
        updated_at=user.get("updated_at")
    )

def create_access_token(data: dict):
    expires_delta = timedelta(minutes=ENV.access_token_expire_minutes)
    token = create_jwt_token(data, expires_delta)
    redis_client.setex(f"token:{token}", int(expires_delta.total_seconds()), data["sub"])
    return token

def logout_user(token: str):
    redis_client.delete(f"token:{token}")