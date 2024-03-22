from db import Base # 데이터베이스를 위한 모델

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255), unique=True)
    active = Column(Boolean, default=False)

    answers = relationship("Answer", back_populates="question")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "active": self.active
        }

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    answer = Column(Boolean, nullable=False)
    
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    question = relationship("Question", back_populates="answers")
    user = relationship("User", back_populates="answers")

    def to_dict(self):
        return {
            "id": self.id,
            "answer": self.answer,
            "question_id": self.question_id,
            "user_id": self.user_id
        }
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), nullable=False, unique=True)
    hashed_password = Column(String, nullable=True)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)

    answers = relationship("Answer", back_populates="user")