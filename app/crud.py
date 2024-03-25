from models import Question, Answer, User
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status, Response
import schemas
from typing import Union, List
import bcrypt
# 데이터 생성(Create)
def create_data(
        model: Union[Question, Answer, User],
        schema,
        db: Session
):
    # 전달된 스키마로부터 데이터를 추출하여 새로운 데이터 객체를 생성
    try:
        data = schema.model_dump()
        if 'password' in data and data['password']:
            hashed_password = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())
            data['hashed_password'] = hashed_password.decode('utf8')
            del data['password']

        insert_data = model(**data)
        # 데이터베이스에 새로운 데이터를 추가
        db.add(insert_data)
        # 변경사항을 데이터베이스에 커밋
        db.commit()
        # 생성된 데이터 반환
        return {'msg': 'Successfully Created'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"error: {e}")

# 데이터 삭제(Delete)
def delete_data(model: Union[Question, Answer, User], id, db: Session):
    # 주어진 ID에 해당하는 데이터를 데이터베이스에서 조회
    data = db.query(model).filter(model.id == id).first()
    # 데이터가 존재하지 않으면 404 오류 발생
    if data is None:
        raise HTTPException(status_code=404, detail="Not Found Error")
    # 데이터 삭제
    db.delete(data)
    # 변경사항을 데이터베이스에 커밋
    db.commit()
    # 삭제 완료 메시지 반환
    return {'msg': 'Successfully deleted'}

def get_all_data(
        model: Union[Question, Answer, User],
        db: Session,
):
    return db.query(model).all()

# 페이징을 적용하여 데이터 조회
def get_datas_by_pagenation(
        model: Union[Question, Answer, User],
        db: Session,
        skip: int,
        limit: int):
    # 페이징을 적용하여 데이터를 조회하고 리스트로 반환
    datas = db.query(model).offset(skip).limit(limit).all()
    # 조회된 데이터가 없으면 빈리스트를 반환
    if not datas:
        return []
        # raise HTTPException(status_code=404, detail=f"{model.__name__}의 데이터가 존재하지 않습니다.")
    return datas

# ID를 기반으로 데이터 조회(Read)
def get_data_by_id(
        model: Union[Question, Answer, User],
        id: int,
        db: Session):
    # 주어진 ID에 해당하는 데이터를 데이터베이스에서 조회
    data = db.query(model).filter(model.id == id).first()
    # 데이터가 존재하지 않으면 404 오류 발생
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found Error")
    # 조회된 데이터 반환
    return data

# 특정 키워드를 포함하는 질문 데이터 검색
def search_question(
        model: Question,
        keyword: str,
        db: Session):
    # ILIKE 연산자를 사용하여 대소문자 구분 없이 키워드를 포함하는 질문 데이터를 검색
    datas = db.query(model).filter(model.content.ilike(f"%{keyword}%")).all()
    # 검색된 데이터가 없으면 404 오류 발생
    if not datas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{keyword}를 포함한 질문이 존재하지 않습니다.")
    return datas

# 데이터 업데이트(Update)
def update_data(
        model: Union[Question, Answer, User],
        id: int,
        schema: schemas.QuestionBase | schemas.AnswerUpdate,
        db: Session):
    # 주어진 ID에 해당하는 데이터를 데이터베이스에서 조회
    data = db.query(model).filter(model.id == id).first()
    # 데이터가 존재하지 않으면 404 오류 발생
    if data:
        # 전달된 스키마로부터 데이터를 추출하여 해당 데이터의 속성을 업데이트
        update_data = schema.model_dump()
        for key, value in update_data.items():
            setattr(data, key, value)
        # 변경사항을 데이터베이스에 커밋
        db.commit()
        # 업데이트된 데이터 반환
        return db.query(model).filter(model.id == id).first()
    # 데이터가 존재하지 않으면 404 오류 발생
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found Error")

def get_answers_by_question_id(
        question_id: int,
        skip: int,
        limit: int,
        db: Session,
):
    datas = db.query(Answer).filter(Answer.question_id == question_id).offset(skip).limit(limit).all()
    if not datas:
        return []
    return datas

def get_answers_by_user_id(
        user_id: int,
        skip: int,
        limit: int,
        db: Session,
):
    datas = db.query(Answer).filter(Answer.user_id == user_id).offset(skip).limit(limit).all()
    if not datas:
        return []
    return datas

def create_answers(data: schemas.AnswerSubmit, db: Session, username: str):
    try:
        user = db.query(User).filter(User.username == username).first()
        user_id = user.id
        for question_id, answer in data.answers.items():
            new_answer = Answer(answer=answer, question_id=question_id, user_id = user_id)
            db.add(new_answer)
            db.commit()
        return {'msg':'Successfully Answer submitted'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"error: {e}")

def get_user_by_username(username, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if user is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username")
    
def activate_question(data: schemas.ActivateQuestion, db: Session):
    for question_id in data.question_ids:
        question = db.query(Question).filter(Question.id == question_id).first()
        if question is not None:
            question.active = True
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid question id")
    db.commit()
    return {'msg': 'Activated Question'}

def deactivate_question(data: schemas.DeactivateQuestion, db: Session):
    for question_id in data.question_ids:
        question = db.query(Question).filter(Question.id == question_id).first()
        if question is not None:
            question.active = False
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid question id")
    db.commit()
    return {'msg': 'Deactivated Question'}

def delete_answers(data: schemas.AnswerDelete, db: Session):
    for id in data.answer_ids:
        answer = db.query(Answer).filter(Answer.id == id).first()
        if answer is not None:
            db.delete(answer)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid answer id")
    db.commit()
    return {'msg': 'Successfully Deleted'}

def get_questions_by_active(db: Session):
    active_questions = db.query(Question).filter(Question.active == True).all()
    if not active_questions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active question")
    questions_dict = [question.to_dict() for question in active_questions]
    return questions_dict

def search_questions(
    keyword: str,
    db: Session
):
    results = db.query(Question).filter(or_(Question.content.like(f"%{keyword}%"))).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{keyword}를 포함한 질문이 존재하지 않습니다.")
    # return [question.to_dict() for question in results]
    return results

def search_user(
    keyword: str,
    db: Session
):
    results = db.query(User).filter(or_(User.username.like(f"%{keyword}%"))).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{keyword}를 포함한 유저가 존재하지 않습니다.")
    return [user.to_dict() for user in results]