from fastapi import FastAPI, Request
from routers.admin import router as admin_router
from routers.survey import router as survey_router
from routers.user import router as user_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory='static/templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(admin_router, prefix='/admin')
app.include_router(survey_router, prefix='/survey')
app.include_router(user_router, prefix='/user')

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level="debug", reload=True)