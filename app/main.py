from fastapi import FastAPI
from routers.admin import router as admin_router
from routers.survey import router as survey_router
app = FastAPI()

app.include_router(admin_router, prefix='/admin')
app.include_router(survey_router, prefix='/survey')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level="debug", reload=True)