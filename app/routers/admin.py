from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import dependencies
from schemas import QuestionBase, AnswerBase, AnswerCreate, AnswerUpdate
from models import Question, Answer
import crud
router = APIRouter()
templates = Jinja2Templates(directory="static/templates")

@router.get('/', response_class=HTMLResponse)
def index(
    request: Request,
    db: Session = Depends(dependencies.get_db)):
    question_data = crud.get_datas_by_pagenation(model=Question, skip=0, limit=5, db=db)
    answer_data = crud.get_datas_by_pagenation(model=Answer, skip=0, limit=5, db=db)
    return templates.TemplateResponse('admin.html', {'request': request, 'question_data': question_data, 'answer_data': answer_data})

@router.post("/qustions")
def create_question(
    question: QuestionBase,
    db: Session = Depends(dependencies.get_db)
):
    return crud.create_data(model=Question, schema=question, db=db)

@router.get("/qustions")
def get_questions(
    skip: int,
    limit: int,
    db: Session = Depends(dependencies.get_db),
):
    return crud.get_datas_by_pagenation(model=Question, skip=skip, limit=limit, db=db)

@router.get('/qustions/{question_id}')
def get_question(
    question_id: int,
    db: Session = Depends(dependencies.get_db),
):
    return crud.get_data_by_id(model=Question, id=question_id, db=db)

@router.put("/qustions/{question_id}")
def update_question(
    question_id: int,
    question: QuestionBase,
    db: Session = Depends(dependencies.get_db)
):
    return crud.update_data(model=Question, id=question_id, schema=question, db=db)

@router.delete("/qustions/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(dependencies.get_db)
):
    return crud.delete_data(model=Question, id=question_id, db=db)

@router.post("/answers")
def create_answer(
    answer: AnswerCreate,
    db: Session = Depends(dependencies.get_db)
):
    return crud.create_data(model=Answer, schema=answer, db=db)

@router.get("/answers")
def get_answers(
    skip: int,
    limit: int,
    db: Session = Depends(dependencies.get_db)
):
    return crud.get_datas_by_pagenation(model=Question, skip=skip, limit=limit, db=db)

@router.get('/answers/{question_id}')
def get_answers_by_question_id(
    question_id: int,
    skip: int,
    limit: int,
    db: Session = Depends(dependencies.get_db)
):
    return crud.get_answers_by_question_id(model=Answer, question_id=question_id, skip=skip, limit=limit, db=db)

@router.put("/answers/{answer_id}")
def update_answer(
    answer_id: int,
    answer: AnswerUpdate,
    db: Session = Depends(dependencies.get_db)    
):
    return crud.update_data(model=Answer, id=answer_id, schema=answer, db=db)

@router.delete("/answers/{answer_id}")
def delete_answer(
    answer_id: int,
    db: Session = Depends(dependencies.get_db)
):
    return crud.delete_data(model=Answer, id=answer_id, db=db)
    