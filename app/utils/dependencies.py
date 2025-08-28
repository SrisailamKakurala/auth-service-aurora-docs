from fastapi import Depends, HTTPException, status # type: ignore
from fastapi.security import OAuth2PasswordBearer # type: ignore
from jose import JWTError, jwt # type: ignore
from app.config.env import ENV
from app.config.database import get_database
from app.config.redis_client import redis_client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = redis_client.get(f"token:{token}")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    try:
        payload = jwt.decode(token, ENV.secret_key, algorithms=[ENV.algorithm])
        username_from_token: str = payload.get("sub")
        if username_from_token != username.decode() if isinstance(username, bytes) else username_from_token != username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token mismatch")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    db = get_database()
    username_str = username.decode() if isinstance(username, bytes) else username
    user = await db.users.find_one({"username": username_str})
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return {
        "user": {
            "id": str(user["_id"]), 
            "username": user["username"], 
            "email": user["email"]
        }, 
        "token": token
    }