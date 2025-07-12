# This file contains the endpoints for logging in of a user.

from fastapi import FastAPI, status, APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
import schemas.schemas_user as schemas_user, models
from database import get_db
from passlib.context import CryptContext
import oauth2

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

router = APIRouter(
    prefix="/login",
    tags=["authorization"]
)

@router.post("/")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user =  db.query(models.Users).filter(models.Users.email_id == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not pwd_context.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
