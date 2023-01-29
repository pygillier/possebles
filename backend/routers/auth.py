from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from backend.settings import app_settings
from backend.database import schemas
from backend.services.users import UserService
from backend.dependencies import security
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


#
@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), svc: UserService = Depends()):
    logger.info("Trying to authenticate user")
    user = security.authenticate_user(svc, form_data.username, form_data.password)
    if user is False:
        logger.error("Unknown user {} or wrong password", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=app_settings.token_expire_minutes)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}