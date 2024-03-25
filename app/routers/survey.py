from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from auth import get_current_user
from typing import Annotated
import dependencies
import schemas
import models
import crud
from services.statistics import GraphGenerator

router = APIRouter()
templates = Jinja2Templates(directory='static/templates')

@router.get('/')
async def testpage(
    request: Request,
    # current_user: Annotated[schemas.UserBase, Depends(get_current_user)],
    db: Session = Depends(dependencies.get_db)
):
    return templates.TemplateResponse('survey.html', {'request': request})

@router.get('/getActiveQuestions')
async def get_active_questions(
    current_user: Annotated[schemas.UserBase, Depends(get_current_user)],
    db: Session = Depends(dependencies.get_db)
):
    return crud.get_questions_by_active(db=db)

@router.get('/results', response_class=HTMLResponse)
async def show_stats(
    request: Request,
    db: Session = Depends(dependencies.get_db)
):
    plot_generator = GraphGenerator()
    graph_data = plot_generator.generate_graphs(db=db)

    return templates.TemplateResponse('result.html', {
        'request': request, 
        'answer_by_age_pie': graph_data['answer_by_age_pie_chart'],
        'answer_by_gender': graph_data['answer_by_gender_chart'],
        'answer_ratio_bar': graph_data['answer_bar_chart'],
        })

@router.post("/submit")
async def submit_answer(
    schema: schemas.AnswerSubmit,
    current_user: Annotated[schemas.UserBase, Depends(get_current_user)],
    db: Session = Depends(dependencies.get_db)
):
    result = crud.create_answers(data=schema, db=db, username=current_user.username)
    print(result)
    return result
