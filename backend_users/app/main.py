from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Users API", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/users",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_in: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.UserResponse:
    try:
        user = crud.create_user(db, user_in)
        return user
    except crud.UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@app.get("/users", response_model=List[schemas.UserResponse])
def list_users(db: Session = Depends(get_db)) -> List[schemas.UserResponse]:
    users = crud.get_users(db)
    return users


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int, db: Session = Depends(get_db)
) -> schemas.UserResponse:
    try:
        user = crud.get_user_by_id(db, user_id)
        return user
    except crud.UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
) -> schemas.UserResponse:
    try:
        user = crud.update_user(db, user_id, user_in)
        return user
    except crud.UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except crud.UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, db: Session = Depends(get_db)
) -> None:
    try:
        crud.delete_user(db, user_id)
    except crud.UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@app.post("/login", response_model=schemas.UserResponse)
def login(
    credentials: schemas.UserLogin, db: Session = Depends(get_db)
) -> schemas.UserResponse:
    try:
        user = crud.authenticate_user(
            db, credentials.username, credentials.password
        )
        return user
    except crud.InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend_users.app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

