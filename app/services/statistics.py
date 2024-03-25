from sqlalchemy.orm import Session
from models import Answer, Question, User
import plotly.graph_objects as go
import pandas as pd


class GraphGenerator:
    def get_data(self, db: Session):
        """
        데이터를 가져와서 pandas 데이터프레임으로 변환하는 메소드.
        """
        # 활성화된 질문만 필터링하여 데이터를 가져옵니다.
        active_questions = db.query(Question).filter(Question.active == True).all()

        # 질문, 답변 및 사용자 정보를 조인하여 데이터를 가져옵니다.
        data = []
        for question in active_questions:
            query_data = db.query(Answer, User). \
                join(User, Answer.user_id == User.id). \
                filter(Answer.question_id == question.id)

            for answer, user in query_data:
                data.append({
                    "Question ID": question.id,
                    "Question": question.content,
                    "Gender": user.gender,
                    "Age": user.age,
                    "Answer": answer.answer
                })
        # 색인된 데이터를 pandas의 데이터프레임으로 반환합니다.
        return pd.DataFrame(data)

    def generate_graphs(self, db: Session):
        data_df = self.get_data(db=db)
        """
        모든 질문에 대해 그래프를 생성하는 메소드.
        return : 그래프들을 HTML로 변환한 리스트
        """
        graphs = {}
        gender_bar_chart_list = []
        age_pie_chart_list = []
        answer_bar_chart_list = []

        # 각 질문에 대해 그래프를 생성
        # 데이터프레임에서 question_id 별로 그룹핑해서 반복문을 돌린다.
        for question_group_id, question_group in data_df.groupby("Question ID"):
            question_text = question_group['Question'].iloc[0]

            # 성별에 따른 답변 막대 그래프를 만들고 리턴할 graphs리스트에 포함하기
            gender_bar_chart_list.append(
                self.answers_by_gender_bar_chart(question_group, question_text)
                )
            # 답변 비율 막대 그래프를 만들고 리턴할 graphs리스트에 포함하기
            answer_bar_chart_list.append(
                self.answer_ratio_bar_chart(question_group, question_text)
            )
            # 나이 그룹에 따른 답변 원형 그래프를 만들고 리턴할 graphs리스트에 포함하기
            age_pie_chart_list.append(
                self.age_group_answer_pie_chart(question_group, question_text)
            )

        graphs['answer_by_gender_chart'] = gender_bar_chart_list
        graphs['answer_bar_chart'] = answer_bar_chart_list
        graphs['answer_by_age_pie_chart'] = age_pie_chart_list

        return graphs

    def answers_by_gender_bar_chart(self, question_group, question_text):
        """
        성별에 따른 답변을 나타내는 막대 그래프를 생성하는 메소드.
        :param question_group: 질문 그룹에 해당하는 데이터프레임
        :return: 막대 그래프를 HTML로 변환한 문자열
        """

     # 성별과 답변을 기준으로 그룹화하여 각 답변에 대한 성별 비율을 계산합니다.
        gender_counts = question_group.groupby(["Answer", "Gender"]).size().unstack(fill_value=0)
        total_counts = gender_counts.sum(axis=1)
        percentages = gender_counts.div(total_counts, axis=0) * 100

        # 막대 그래프를 생성합니다.
        fig = go.Figure()
        for gender in gender_counts.columns:
            fig.add_trace(go.Bar(x=['true','false'], y=percentages[gender], name=gender))

        fig.update_layout(
            title=f'Q. {question_text}',
            xaxis=dict(title='Answer'),
            yaxis=dict(title='Percentage'),
            barmode='group',
            legend=dict(title='Gender')
        )

        return fig.to_html()

    def answer_ratio_bar_chart(self, question_group, question_text):
        """
        답변 비율을 나타내는 막대 그래프를 생성하는 메소드입니다.
        :param question_group: 질문 그룹에 해당하는 데이터프레임
        :return: 막대 그래프를 HTML로 변환한 문자열
        """
        # 답변 비율을 계산하여 막대 그래프를 생성
        answer_counts = question_group["Answer"].value_counts()
        
        # 전체 응답 수를 구함
        total_responses = answer_counts.sum()
        
        # 퍼센티지를 계산
        percentages = [(count / total_responses) * 100 for count in answer_counts.values]
        
        # 막대 그래프를 생성
        fig = go.Figure(data=[go.Bar(x=answer_counts.index, y=answer_counts.values, marker_color=['blue', 'red'])])
        
        # x축에 퍼센티지를 추가
        fig.update_xaxes(
            tickvals=[True, False], 
            ticktext=[f'{idx} ({percentage:.1f}%)' for idx, percentage in zip(answer_counts.index, percentages)]
            )
        
        fig.update_layout(title=f'Q. {question_text}')
        return fig.to_html()

    def age_group_answer_pie_chart(self, question_group, question_text):
        """
        나이 그룹에 따른 답변을 나타내는 원형 그래프를 생성하는 메소드입니다.
        :param question_group: 질문 그룹에 해당하는 데이터프레임
        :return: 원형 그래프를 HTML로 변환한 문자열
        """
        # 나이 그룹에 따른 답변을 계산하여 원형 그래프를 생성합니다.
        question_group["Age Group"] = question_group["Age"] // 10 * 10
        age_group_counts = question_group["Age Group"].value_counts()
        labels = [f"{age}-{age+9}" for age in sorted(age_group_counts.index)]
        values = age_group_counts.values
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(title=f'Q. {question_text}')
        return fig.to_html()
