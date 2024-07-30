from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ..form import QuestionForm
from ..models import Question


@login_required(login_url='common:login')
def question_vote(request,question_id):
    # 1에 작성하려면 구별을해야하기때문에 id를가져옴
    question=get_object_or_404(Question,pk=question_id)
    if request.user == question.author:
        messages.error(request,'본인글은 추천x')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail',question.id)
    # vote는 question과 1:다 기때문에 question_id에 연결되어서 참조가되어야함
    # question id를 꺼내와야 voter를 할수가있다 다:1관계이기때문에 question(1)
    # 을꺼내서 다(vote)를 넣는식으로 함

@login_required(login_url='common:login')
def question_create(request):
    # 질문등록하기눌러서 get방식으로 화면렌더링하는게있고
    # post를눌러서 model을 등록하는게있음
    # 그러므로 구별해야함
    if request.method == "POST":
        form=QuestionForm(request.POST)

        print(request.POST)
        if form.is_valid():
            
            question=form.save(commit=False)
            question.author=request.user
            # request.user=anonymouseuser 아까 model에서 틀리게 적어서 자동으로
            # 그렇게세팅됨
            # 임시저장만하라 아직 저장은하지말라라는뜻 모델에 subject,content만있어서
            # datetime은없기때문 다하고 save를한다
            question.create_date=timezone.now()
            question.save()
            return redirect('pybo:index')
    else: 
        # request.method=='get'이라고보면됨
        form=QuestionForm()
    context={'form':form}
    return render(request,'pybo/question_form.html',context)
    
@login_required(login_url='common:login')
def question_modify(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    if request.user != question.author:
        messages.error(request,'수정권한이 없음')
        return redirect('pybo:detail',question_id=question.id)
    if request.method == "POST":
        form=QuestionForm(request.POST,instance=question)
        if form.is_valid():
            question=form.save(commit=False)
            question.modify_date=timezone.now()  
            question.save()
            return redirect('pybo:detail',question_id=question.id)
        
    else:
        form=QuestionForm(instance=question)
    context={'form':form}
    return render(request,'pybo/question_form.html',context)


@login_required(login_url='common:login')
def question_delete(request,question_id):
    quesiton=get_object_or_404(Question,pk=question_id)
    if request.user != quesiton.author:
        messages.error('삭제권한없음')
        return redirect('pybo:detail',quesiton.id)
    quesiton.delete()
    return redirect('pybo:index')
