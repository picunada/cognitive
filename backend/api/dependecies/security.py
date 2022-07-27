from datetime import timedelta, datetime
from typing import Union

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status

from core.config import Settings
from models.client import Client_Pydantic, ClientModel
from models.manager import ManagerModel, Manager_Pydantic

X_API_KEY = APIKeyHeader(name='X-API-Key')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/manager/auth")

settings = Settings()


async def api_key_auth(x_api_key: str = Depends(X_API_KEY)) -> Client_Pydantic:
    if not x_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not valid api-key")
    client_obj = await ClientModel.get_or_none(api_key__api_key=x_api_key).prefetch_related('api_key')
    return await Client_Pydantic.from_tortoise_orm(client_obj)


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str):
    manager = await Manager_Pydantic.from_queryset_single(ManagerModel.get(email=email))
    if not manager:
        return False
    if not await verify_password(password, manager.hashed_password):
        return False
    return manager


async def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    manager = ManagerModel.get(email=email)
    if manager is None:
        raise credentials_exception
    return manager
