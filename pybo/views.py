
from email import message

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from pybo.form import AnswerForm, QuestionForm
from pybo.models import Answer, Question


# Create your views here.
def index(request):
    page=request.GET.get('page','1')
    # pybo/?page=1처럼 값을가져올때 사용
    # request.get할텐데 page=1로 사용하라
    # 없을경우 default로 1로 사용하라는뜻
    # request는 컨트롤러로부터 model을 담은 매개변수라고보면되나?
    question_list=Question.objects.order_by('-create_date')
    paginator=Paginator(question_list,10)
    # 10개까지자른것만 page_obj에서 기본으로 보여라
    # 전체틀은 10씩이고
    # 페이지당 보여줄 개수
    page_obj=paginator.get_page(page)
    question_list=page_obj
    question_list.has_previous
    question_list.has_next
    question_list.number
    question_list.paginator.page_range
    question_list.previous_page_number
    question_list.next_page_number
    question_list.paginator.count
    question_list.start_index
    
    # 이렇게 옵젝으로 설정안하고 속성안하면 html에서 다음으로 못넘어가기때문 
    # page1기본값을 page_obj에 넣음
    # page_obj= 10개중에 일단 get_page 초기값 1로 보여줌
    # 객체를 생성해서 데이터만 조회하도록 쿼리,즉 속성할당하기위해씀
    # 속성을 html에 적용하기위해 context에 전달
    context={'question_list':page_obj}
    
    
    # context={'question_list':question_list}
    return render(request,'pybo/question_list.html',context)

def detail(request,question_id):
    # 자료형만가져오는거고 실질적으로는 controlleㄱ에서 받아오는것
    question=get_object_or_404(Question,pk=question_id)
    question.content

    question.answer_set.count
    context={'question':question}
    return render(request,'pybo/question_detail.html',context)

# 로그인화면으로 들어가라 만일안될경우

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
        return redirect('pybo:detail',answer.question.id)
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
            return redirect('pybo:detail',question.id)
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