from db import Base # 데이터베이스를 위한 모델

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, unique=True)

    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    anwswer = Column(Boolean, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    job = Column(String, default=None)

    question_id = Column(Integer, ForeignKey("questions.id"))

    question = relationship("Question", back_populates="answers")