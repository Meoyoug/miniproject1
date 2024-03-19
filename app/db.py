from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# # 비동기용 데이터 베이스 설정 -> asyncpg
# ASYNC_SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://meoyong:eodyd456@fastapi_miniproject-db-1:5432/mp_test"
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, echo=True)
# AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# Base = declarative_base()

# 동기용 데이터 베이스 설정 -> psycopg2
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://meoyong:eodyd456@fastapi_miniproject-db-1:5432/mp_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

Base = declarative_base()
# 아무리 코드가 비동기여도 데이터베이스를 동기로 설정하면 orm, 쿼리 과정에서는 동기로 적용된다
# 따라서 만약 비동기식으로 작업을 수행하는 코드작성시 데이터베이스 설정할 때 비동기로 설정해주는 것이 중요하다.