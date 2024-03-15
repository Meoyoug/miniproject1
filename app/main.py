from fastapi import FastAPI, Depends
from routers.admin import router as admin_router
from dependencies import get_db

app = FastAPI()

app.include_router(admin_router, prefix='/admin')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', port=8000, log_level="debug", reload=True)