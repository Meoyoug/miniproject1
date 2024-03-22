from fastapi import Depends
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px # 그래프로 그려주고 보여줌
from sqlalchemy import case, func
from sqlalchemy.orm import Session
from models import Answer, Question, User
import dependencies

class AnswerPlotlyGraph():

    def get_acitve_question_ids(db: Session):
        query_result = db.query(Question.id).filter(Question.active == True).all()
        print(query_result)
    
    # def get_answer_counts_by_question(self):
    @classmethod
    def make_bar_charts_by_question(self, db: Session):
        results = []
        # 각 질문별로 예(True)와 아니오(False)에 대한 답변 수를 가져옴
        query_result = (
            db.query(Question.content, 
                                  func.sum(case((Answer.answer == True, 1), else_=0)).label('Yes'),
                                  func.sum(case((Answer.answer == False, 1), else_=0)).label('No'))
            .join(Answer)
            .group_by(Question.id)
            .all()
        )

        for question_content, yes_count, no_count in query_result:
            df = pd.DataFrame({'Response': ['Yes', 'No'], 'Count': [yes_count, no_count]})
            fig = px.bar(df, x='Response', y='Count', color='Response', title=f'Responses for Question: {question_content}', width=1000, height=600)
            results.append(fig.to_html())

        return results

    @classmethod
    def make_bar_charts_by_gender(self, db: Session):
        results = []
        # 각 성별별로 예(True)와 아니오(False)에 대한 답변 수를 가져옴
        query_result = (
            db.query(Answer, User.gender)
            .join(User)
            .filter(Answer.question_id == Question.id)
            .all()
        )

        for gender, question_content, yes_count, no_count in query_result:
            df = pd.DataFrame({'Response': ['Yes', 'No'], 'Count': [yes_count, no_count]})
            fig = px.bar(df, x='Response', y='Count', color='gender', title=f'Responses for Question: {question_content} (Gender: {gender})', width=1000, height=600)
            results.append(fig.to_html())

        return results
    

    