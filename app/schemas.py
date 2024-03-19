from pydantic import BaseModel
from typing import Optional, List

class QuestionBase(BaseModel):
    content: str

    class Config:
        from_attributes = True

class AnswerBase(BaseModel):
    answer: bool
    gender: str
    age: int
    job: Optional[str] = None
    question_id: int

    class Config:
        from_attributes = True

class AnswerCreate(AnswerBase):
    pass

class AnswerUpdate(AnswerBase):
    answer: bool | None=None
    gender: str | None=None
    age: int | None=None
    job: str | None=None
    question_id: int

class AnswerSubmit(AnswerBase):
    question_id: List[int]
    answer: List[bool]
    