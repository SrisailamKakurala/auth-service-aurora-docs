from jose import jwt # type: ignore
from datetime import datetime, timedelta, timezone
from app.config.env import ENV

def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ENV.secret_key, algorithm=ENV.algorithm)
    return encoded_jwt