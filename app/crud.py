from models import Question, Answer
from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas import QuestionBase, AnswerUpdate

# 데이터 생성(Create)
def create_data(model: Question | Answer, schema, db: Session):
    # 전달된 스키마로부터 데이터를 추출하여 새로운 데이터 객체를 생성
    data = model(**schema.model_dump())
    # 데이터베이스에 새로운 데이터를 추가
    db.add(data)
    # 변경사항을 데이터베이스에 커밋
    db.commit()
    # 생성된 데이터 반환
    return schema

# 데이터 삭제(Delete)
def delete_data(model: Question | Answer, id, db: Session):
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

# 페이징을 적용하여 데이터 조회
def get_datas_by_pagenation(
        model: Question | Answer,
        db: Session,
        skip: int,
        limit: int):
    # 페이징을 적용하여 데이터를 조회하고 리스트로 반환
    datas = db.query(model).offset(skip).limit(limit).all()
    # 조회된 데이터가 없으면 404 오류 발생
    if not datas:
        return []
        # raise HTTPException(status_code=404, detail=f"{model.__name__}의 데이터가 존재하지 않습니다.")
    return datas

# ID를 기반으로 데이터 조회(Read)
def get_data_by_id(
        model: Question | Answer,
        id: int,
        db: Session):
    # 주어진 ID에 해당하는 데이터를 데이터베이스에서 조회
    data = db.query(model).filter(model.id == id).first()
    # 데이터가 존재하지 않으면 404 오류 발생
    if data is None:
        raise HTTPException(status_code=404, detail="Not Found Error")
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
        raise HTTPException(status_code=404, detail=f"{keyword}를 포함한 질문이 존재하지 않습니다.")
    return datas

# 데이터 업데이트(Update)
def update_data(
        model: Question | Answer,
        id: int,
        schema: QuestionBase | AnswerUpdate,
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
    raise HTTPException(status_code=404, detail="Not Found Error")

def get_answers_by_question_id(
        model: Question,
        question_id: int,
        skip: int,
        limit: int,
        db: Session,
):
    datas = db.query(model).filter(model.question_id == question_id).offset(skip).limit(limit).all()
    return datas

def create_answers(data: dict, db: Session):
    results = []
    for question_id, answer in zip(data['question_id'], data['answer']):
        new_answer = Answer(answer=answer, question_id=question_id, age=data['age'], gender=data['gender'])
        if data.get('job'):
            new_answer.job = data['job']
        db.add(new_answer)
        db.commit()
        db.refresh(new_answer)
        results.append(new_answer.to_dict())
    return results