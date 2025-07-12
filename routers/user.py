# This file contains endpoints for creating and viewing of a user.

from fastapi import FastAPI, status, APIRouter, HTTPException, Depends
from sqlmodel import Session
import schemas.schemas_user as schemas_user, models
from database import get_db
from passlib.context import CryptContext
import oauth2

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get("/profile", response_model=schemas_user.user_display, status_code=status.HTTP_200_OK)
def profile(current_user: models.Users = Depends(oauth2.get_current_user)):
    return current_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model = schemas_user.user_display)
def display_user_info(id: int , db: Session = Depends(get_db)):
    user = db.query(models.Users).filter( models.Users.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such user exist")
    return user

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model= schemas_user.user_display)
def create_user(user:schemas_user.user_create, db: Session=Depends(get_db)):
    user.password = pwd_context.hash(user.password)
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

