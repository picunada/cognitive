from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from api.dependecies.security import authenticate_user, create_access_token, get_password_hash
from core.config import Settings
from models.manager import ManagerIn_Pydantic, ManagerModel, Manager_Pydantic
from schemas.auth import Token, TokenOnReg
from schemas.manager import ManagerCreate

router = APIRouter()
settings = Settings()


@router.post("/auth", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    manager = await authenticate_user(form_data.username, form_data.password)
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = await create_access_token(
        data={"sub": manager.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get('/', response_model=List[Manager_Pydantic])
async def list_all_managers():
    return await Manager_Pydantic.from_queryset(ManagerModel.all())


@router.post('/', response_model=Manager_Pydantic)
async def create_manager(manager: ManagerCreate):
    manager.password = await get_password_hash(manager.password)
    manager_obj = await ManagerModel.create(email=manager.email, hashed_password=manager.password)
    return await Manager_Pydantic.from_tortoise_orm(manager_obj)
