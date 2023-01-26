import logging
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.dependencies import db, security
from backend.database import models, schemas


logger = logging.getLogger(__name__)


class UserService:
    """Service class for all user-related actions"""

    def __init__(self, sess: Session = Depends(db.get_db)):
        logger.info("FeedService init")
        self._sess = sess

    def get_user(self, user_id: int) -> models.User | None:
        return self._sess.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_email(self, email: str) -> models.User | None:
        return self._sess.query(models.User).filter(models.User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> list[models.User]:
        return self._sess.query(models.User).offset(skip).limit(limit).all()

    def create_user(self, user: schemas.UserCreate) -> models.User:
        hashed_password = security.get_password_hash(user.password)
        db_user = models.User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        self._sess.add(db_user)
        self._sess.commit()
        self._sess.refresh(db_user)

        return db_user
