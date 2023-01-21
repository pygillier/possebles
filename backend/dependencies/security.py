from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.database import crud, models, schemas
from backend.dependencies import db
from backend.settings import app_settings
from datetime import datetime, timedelta
from jose import JWTError, jwt
from loguru import logger


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)

# passlib for password hashing/checks
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(sess: Session, username: str, password: str) -> models.User | bool:
    """Authenticates the user against database & password"""
    user = crud.get_user_by_email(sess, email=username)
    if user is None:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    logger.info("Expires: {}", expire)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        app_settings.token_secret_key,
        algorithm=app_settings.token_algorithm
    )

    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), sess: Session= Depends(db.get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, app_settings.token_secret_key, algorithms=[app_settings.token_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(sess, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
