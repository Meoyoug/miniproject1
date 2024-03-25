from fastapi import APIRouter, Depends, Request, HTTPException, status, Response, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Annotated
from urllib.parse import quote_plus
import dependencies
import schemas
import auth
import models
import crud

router = APIRouter()
templates = Jinja2Templates(directory='static/templates')

@router.get('/', response_class=HTMLResponse)
async def index(
    request: Request,
    db: Session = Depends(dependencies.get_db)):
    question_data = crud.get_datas_by_pagenation(model=models.Question, skip=0, limit=20, db=db)
    answer_data = crud.get_datas_by_pagenation(model=models.Answer, skip=0, limit=20, db=db)
    user_data = crud.get_datas_by_pagenation(model=models.User, skip=0, limit=20, db=db)
    return templates.TemplateResponse('admin.html', {'request': request, 'question_data': question_data, 'answer_data': answer_data, 'user_data': user_data})

@router.post('/token')
async def admin_login(
    user: schemas.LoginUser,
    db: Session = Depends(dependencies.get_db)
) -> schemas.Token:
    user_data = user
    auth_user = auth.authenticate_user(user_data=user_data, db=db)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not auth.is_superuser(auth_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not a superuser")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

@router.post("/questions")
async def create_question(
    question: schemas.QuestionBase,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.create_data(model=models.Question, schema=question, db=db)

@router.get("/questions")
async def get_questions(
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db),
):
    return crud.get_all_data(model=models.Question, db=db)

@router.get('/questions/{question_id}')
async def get_question(
    question_id: int,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db),
):
    return crud.get_data_by_id(model=models.Question, id=question_id, db=db)

@router.put("/questions/{question_id}")
async def update_question(
    question_id: int,
    question: schemas.QuestionBase,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.update_data(model=models.Question, id=question_id, schema=question, db=db)

@router.delete("/questions/{question_id}")
async def delete_question(
    question_id: int,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.delete_data(model=models.Question, id=question_id, db=db)

@router.post("/questions/activate")
async def activate_question(
    data: schemas.ActivateQuestion,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.activate_question(data=data, db=db)

@router.post("/questions/deactivate")
async def deactivate_question(
    data: schemas.DeactivateQuestion,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.deactivate_question(data=data, db=db)

@router.get("/questions/search/{keyword}")
async def search_questions(
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    keyword: str,
    db: Session = Depends(dependencies.get_db)
) -> List[schemas.QuestionSearchResponse]:
    return crud.search_questions(keyword=keyword, db=db)

@router.post("/answers")
async def create_answer(
    answer: schemas.AnswerCreate,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.create_data(model=models.Answer, schema=answer, db=db)

@router.get("/answers")
async def get_answers(
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.get_all_data(model=models.Answer, db=db)

@router.delete('/answers')
async def delete_answers(
    data: schemas.AnswerDelete,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.delete_answers(data=data, db=db)

@router.get('/answers/{question_id}')
async def get_answers_by_question_id(
    question_id: int,
    skip: int,
    limit: int,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.get_answers_by_question_id(model=models.Answer, question_id=question_id, skip=skip, limit=limit, db=db)

@router.put("/answers/{answer_id}")
async def update_answer(
    answer_id: int,
    answer: schemas.AnswerUpdate,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)    
):
    return crud.update_data(model=models.Answer, id=answer_id, schema=answer, db=db)

@router.delete("/answers/{answer_id}")
async def delete_answer(
    answer_id: int,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.delete_data(model=models.Answer, id=answer_id, db=db)

@router.get('/user')
def get_user(
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.get_all_data(model=models.User, db=db)

@router.post('/user')
def create_user(
    user: schemas.UserBase,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.create_data(model=models.User, schema=user, db=db)

@router.delete('/user/{user_id}')
def delete_user(
    user_id: int,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.delete_data(model=models.User, id=user_id, db=db)

@router.get('/user/{user_id}')
def get_user_by_id(
    user_id: int,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.get_data_by_id(model=models.User, db=db, id=user_id)

@router.put('/user/{user_id}')
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.update_data(model=models.User, id=user_id, schema=user, db=db)

@router.get("/user/search/{keyword}")
async def search_questions(
    current_user: Annotated[schemas.UserBase, Depends(auth.get_current_superuser)],
    keyword: str,
    db: Session = Depends(dependencies.get_db)
) -> List[schemas.UserSearchResponse]:
    return crud.search_user(keyword=keyword, db=db)