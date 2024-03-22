from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import dependencies
import models
import crud
import bcrypt
import schemas

# oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="/user/token")
# oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="/admin/token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

SECRET_KEY = "meoyongtesting123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def check_password(password: str, hashed_password: str):
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return True
    return False

def authenticate_user(user_data: dict, db: Session):
    user = crud.get_user_by_username(username=user_data.username, db=db)
    if check_password(user_data.password, user.hashed_password):
        return user
    return False

def is_superuser(user: models.User):
    print(user.is_superuser)
    if user.is_superuser:
        return True
    return False

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(dependencies.get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return schemas.UserBase(username=user.username, age=user.age, gender=user.gender)

async def get_current_superuser(
        current_user: Annotated[schemas.UserBase, Depends(get_current_user)],
        db: Session = Depends(dependencies.get_db)
        ):
    user = db.query(models.User).filter(models.User.username == current_user.username).first() 
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not a superuser"
            )
    return current_user