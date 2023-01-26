from fastapi import APIRouter, HTTPException, Depends
from backend.services.users import UserService
from backend.database import schemas
from backend.dependencies import security
import logging


router = APIRouter(
    prefix="/users",
    tags=["User"]
)

logger = logging.getLogger(__name__)


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, svc: UserService = Depends()):
    db_user = svc.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return svc.create_user(user=user)


@router.get("/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, svc: UserService = Depends()):
    users = svc.get_users(skip=skip, limit=limit)
    return users


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(security.get_current_active_user)):
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, svc: UserService = Depends()):
    db_user = svc.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
