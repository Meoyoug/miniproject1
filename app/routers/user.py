from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import timedelta
from sqlalchemy.orm import Session
from typing import Union
import dependencies
import schemas
import models
import crud
import auth

router = APIRouter()
templates = Jinja2Templates(directory='static/templates')

@router.post('/signup')
async def signup(
    user: schemas.CreateUser,
    db: Session = Depends(dependencies.get_db)
):
    return crud.create_data(model=models.User, schema=user, db=db)

@router.post('/non-member')
async def non_member(
    user: schemas.NonMemberUser,
    db: Session = Depends(dependencies.get_db)
):
    return crud.create_data(model=models.User, schema=user, db=db)

@router.post('/token')
async def login_for_access_token(
    user: Union[schemas.LoginUser, schemas.NonMemberUser],
    db: Session = Depends(dependencies.get_db)
) -> schemas.Token:
    if isinstance(user, schemas.LoginUser):
        user_data = user
        if not auth.authenticate_user(user_data=user_data, db=db):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    if isinstance(user, schemas.NonMemberUser):
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")