
from django.urls import path, re_path

from . import views
from .views import answer_view, base_views, question_view

app_name='pybo'
urlpatterns = [
    # base_views.py
    path('',base_views.index,name='index'),
    path('<int:question_id>/',base_views.detail,name='detail'),
    
    
    path('question/vote/<int:question_id>',question_view.question_vote,name='question_vote'),
    path('question/create/',question_view.question_create,name='question_create'),
    path('question/modify/<int:question_id>/', question_view.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/',question_view.question_delete,name='question_delete'),
    
    path('answer/vote/<int:answer_id>',answer_view.answer_vote,name='answer_vote'),
    path('answer/create/<int:question_id>/',answer_view.answer_create,name='answer_create'),
    path('answer/modify/<int:answer_id>/',answer_view.answer_modify,name='answer_modify'),
    path('answer/delete/<int:answer_id>/',answer_view.answer_delete,name='answer_delete'),
#    forms.from 일반폼과 forms.Modelform은 다름
# 페이지요청시 전달되는 파라미터를 관리하기위한 클래스 
    # 끝에 /를붙여줘야 실행됨/2/이런식으로
    # url과 view조합이 controlleㄱ라고봐야함
]