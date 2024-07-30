from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.utils import timezone

from ..form import AnswerForm
from ..models import Answer, Question


@login_required(login_url='common:login')
def answer_vote(request,answer_id):
    answer=get_object_or_404(Answer,pk=answer_id)
    if request.user == answer.author:
        messages.error(request,'본인 추천 x')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(
            resolve_url('pybo:detail',answer.question.id),answer.id))
# answer.id 하면 주소가달라서 detail question이아닌 다른쪽으로 넘어갈것임
    

@login_required(login_url='common:login')
def answer_modify(request,answer_id):
    # url.py 로부터 answer_id를 기본키에 전달해야함 안그러면 unpack int라고 해서 못찾음
    answer=get_object_or_404(Answer,pk=answer_id)
    if request.user != answer.author:
        messages.error(request,'수정권한x')
        return redirect('pybo:detail',answer.question.id)
    
    if request.method == "POST":
        form=AnswerForm(request.POST,instance=answer)
        if form.is_valid():
            # answer이 answer_id를 가져온게아닌 POST데이터를 가져온 form으로 업뎃함
            answer=form.save(commit=False)
            answer.modify_date=timezone.now()
            answer.save()
        # 트랜잭션 읽,쓰,수를 한단위로 실행하며 하나라도 실패하는순간 되돌아감 and연산 중요
        # save()는 트랜잭션에서 필수요소 save()가 안되면 트랜잭션이 완성안되므로  에러가뜸
        return redirect('{}#answer_{}'.format(
            resolve_url('pybo:detail',answer.question.id),answer.id))
    else:
        form=AnswerForm(instance=answer)
    context={'answer':answer,'form':form}
            # answer은 현재,과거를 하려는거고
            # form은 내가 막 입력하거나 수정하려할때 쓰는거라고봐야함
    return render(request,'pybo/answer_form.html',context)   
        # instance는 채워주기도하며 기존에있는 instaceㅇ레코드를 연결하는 걸 뜻함

@login_required(login_url='common:login')
def answer_create(request,question_id):
    
    question=get_object_or_404(Question,pk=question_id)
    # question.answer_set.create(content=request.POST.get('content'),create_date=timezone.now())
    if request.method == "POST":
        # post클릭시 form에 post를 넣는다. 반응을넣음
        form=AnswerForm(request.POST)
        if form.is_valid():
            
            answer=form.save(commit=False)
            answer.author=request.user
            
            answer.create_date=timezone.now()
            answer.question=question
            answer.save()
            redirect('{}#answer_{}'.format(
            resolve_url('pybo:detail',answer.question.id),answer.id))
    else:
        form=AnswerForm()
    context={'question':question,'form':form}
    return render(request,'pybo/question_detail.html',context)

        # post는 render할필요없음 왜냐하면 안에서 model을 생성하기때문
        
    
        
    # request.POST는 넣은것 여기서 get(매개변수)해서 답변내용을 가져옴 textarea
    
# html상에서 post가들어있으면 굳이 post로부터 받아오는거기때문에 render로 context를 전달안해도되는것
# render해서 가져오는 값이없으므로 redirect로 다른곳으로 가고됨

@login_required(login_url='common:login')
def answer_delete(request,answer_id):
    # url.py 변수랑 일치해야함 위의 argument가
    # 또한 form은 입력필드를 자동제공해주며, 필드와 오류메세지등을 렌더링하는데도
    # 주요사용됨 입력일단 시킬려면 model form을 써야함 
    answer=get_object_or_404(Answer,pk=answer_id)
    if request.user != answer.author:
        messages.error(request,'삭제권한x')
    else:
        answer.delete()
    return redirect('pybo:detail',question_id=answer.question.id)
 # request:httprequest형식
# request.POST는 눌렀을때 반영되는 데이터를 뜻함
# request는 뭘하기직전의 상태를 뜻한다고봐도됨
# 빈껍대기를 html에 