from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import dependencies
import schemas
from models import Question, Answer
import crud
from services.statistics import AnswerPlotlyGraph

router = APIRouter()
templates = Jinja2Templates(directory='static/templates')

@router.get('/', response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(dependencies.get_db)):
    plotly_tool = AnswerPlotlyGraph
    answer_plotdata = plotly_tool.make_pie_chart(db=db)
    return templates.TemplateResponse('result.html', {'request': request, 'question_plots': answer_plotdata})

@router.post("/submit")
def submit_answer(
    schema: schemas.AnswerSubmit,
    db: Session = Depends(dependencies.get_db)
):
    data = schema.model_dump()
    result = crud.create_answers(data, db=db)
    print(result)
    return result

@router.get('/results')
def show_results():
    
    return templates.TemplateResponse()