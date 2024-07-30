from django import forms

from pybo.models import Answer, Question


# forms.ModelForm=request.post 와 같은형태 request.post= 모델폼이다
# 이러한형태를 가져옴
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        # fiels 리스트
        # 레이블 딕셔너리
        labels={
            'content':'답변내용'
        }
# modelform
class QuestionForm(forms.ModelForm):
    class Meta:
        # view에서 호출하면 model데이터를 저장하게 할수있음 
        model = Question
        # subject는 charfiled에서 모델타입, content는 textfiled타입으로되어있어서
        #  모델폼으로 필드지정할경우 input type으로 자동할당
        fields = ['subject','content']
        
        labels={
            'subject':'제목',
            'content':'내용'
        }