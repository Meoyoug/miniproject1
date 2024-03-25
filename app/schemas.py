from pydantic import BaseModel
from typing import Optional, List

class QuestionBase(BaseModel):
    content: str

    class Config:
        from_attributes = True

class ActivateQuestion(BaseModel):
    question_ids: List[int]

class DeactivateQuestion(ActivateQuestion):
    pass

class AnswerBase(BaseModel):
    answer: bool
    question_id: int

    class Config:
        from_attributes = True

class AnswerCreate(AnswerBase):
    pass

class AnswerUpdate(AnswerBase):
    answer: bool
    question_id: int

class AnswerDelete(BaseModel):
    answer_ids: List[int]

class AnswerSubmit(BaseModel):
    answers: dict[int, bool]
    
class UserBase(BaseModel):
    username: str
    age: int
    gender: str

    class Config:
        from_attributes = True

class CreateUser(UserBase):
    password: str

class LoginUser(BaseModel):
    username: str
    password: str

class UserUpdate(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    
class NonMemberUser(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserSearchResponse(UserBase):
    id : int
    is_superuser: bool

class QuestionSearchResponse(QuestionBase):
    id: int
    active: bool
