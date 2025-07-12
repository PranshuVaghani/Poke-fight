# This includes the utility functions for authorization ( auth.py ).
# User authentication.

from datetime import datetime,timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import schemas.schemas_user as schemas_user, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = "BEHAPPY"
ALGORITHM = "HS256"
TOKEN_EXPIRY_TIME= 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(TOKEN_EXPIRY_TIME)
    to_encode.update({"exp": expire})

    encoded_jwt =  jwt.encode(to_encode,SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = decoded_jwt.get("user_id")
        if id is None:
            raise credentials_exception
        token_data= schemas_user.TokenData(id = str(id))
    
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: database.Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Unauthorized", headers={"WWW-Authenticate": "Bearer"})
    token = verify_token(token, credential_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    if not user:
        raise credential_exception
    
    return user
