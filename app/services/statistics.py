import pandas as pd
import numpy as np
import plotly as pl
import plotly.graph_objects as go
import plotly.express as px # 그래프로 그려주고 보여줌
import plotly.io as pio
from sqlalchemy.orm import Session
from models import Answer, Question
import dependencies
from fastapi import Depends

class AnswerPlotlyGraph():
    def make_pie_chart(db: Session):
        datas = db.query(Answer).all()
        column_names = Answer.__table__.columns.keys()
        datas = [data.to_dict() for data in datas]
        results = []
        df = pd.DataFrame(datas, columns=column_names)

        for column in column_names:
            fig = px.pie(df, values=f'{column}', names='answer', title = f'Answers By {column} Rating')
            html = fig.to_html()
            results.append(html)
        return results        


    
    