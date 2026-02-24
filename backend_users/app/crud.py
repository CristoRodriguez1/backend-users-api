from typing import List, Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import models, schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


def _get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_id(db: Session, user_id: int) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise UserNotFoundError(f"User with id {user_id} not found")
    return user


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    existing_by_username = get_user_by_username(db, user_in.username)
    if existing_by_username is not None:
        raise UserAlreadyExistsError("Username already registered")

    existing_by_email = get_user_by_email(db, user_in.email)
    if existing_by_email is not None:
        raise UserAlreadyExistsError("Email already registered")

    hashed_password = _get_password_hash(user_in.password)
    db_user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate) -> models.User:
    db_user = get_user_by_id(db, user_id)

    if user_in.username is not None and user_in.username != db_user.username:
        other = (
            db.query(models.User)
            .filter(models.User.username == user_in.username, models.User.id != user_id)
            .first()
        )
        if other is not None:
            raise UserAlreadyExistsError("Username already registered")
        db_user.username = user_in.username

    if user_in.email is not None and user_in.email != db_user.email:
        other = (
            db.query(models.User)
            .filter(models.User.email == user_in.email, models.User.id != user_id)
            .first()
        )
        if other is not None:
            raise UserAlreadyExistsError("Email already registered")
        db_user.email = user_in.email

    if user_in.password is not None:
        db_user.hashed_password = _get_password_hash(user_in.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    db_user = get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()


def authenticate_user(db: Session, username: str, password: str) -> models.User:
    user = get_user_by_username(db, username)
    if user is None:
        raise InvalidCredentialsError("Invalid credentials")

    if not _verify_password(password, user.hashed_password):
        raise InvalidCredentialsError("Invalid credentials")

    return user

