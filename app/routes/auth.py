from fastapi import APIRouter, Depends, HTTPException, status # type: ignore
from fastapi.security import OAuth2PasswordRequestForm # type: ignore
from app.services.auth import register_user, authenticate_user, create_access_token, logout_user
from app.utils.dependencies import get_current_user
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=Token)
async def register(form_data: UserCreate):
    user = await register_user(form_data.username, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    logout_user(current_user["token"])
    return {"message": "Successfully logged out"}

@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user["user"]