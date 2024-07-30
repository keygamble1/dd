from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from ..models import Question


# Create your views here.
def index(request):
    page=request.GET.get('page','1')
    kw=request.GET.get('kw','')
    # 기본값 '' ,1
    # get('id',기본값) 으로 정함
    
    # pybo/?page=1처럼 값을가져올때 사용
    # request.get할텐데 page=1로 사용하라
    # 없을경우 default로 1로 사용하라는뜻
    # request는 컨트롤러로부터 model을 담은 매개변수라고보면되나?
    question_list=Question.objects.order_by('-create_date')
    
    if kw:
        question_list=question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
        
        pass
    # d
    # git init 초기화부터하고, gitstatus하면 빈폴더만나옴
    #  git add *해야 파일까지다 넣는거고 gitstatus하면 주즈륵나옴
    # .idea나 db.sqlite는 사옹자,시스템별로 달라지기때문에 깃으로 관리하면 x
    # .idea = 파이참, db.sqlite=sqlite 데이터베이스 파일
    # 사용자 개인 데이터 는 다빼야함 오직템플릿만
    paginator=Paginator(question_list,10)
    page_obj=paginator.get_page(page)
    context={'question_list':page_obj,'page':page,'kw':kw}
    return render(request,'pybo/question_list.html',context)
    # 10개까지자른것만 page_obj에서 기본으로 보여라
    # 전체틀은 10씩이고
    # 페이지당 보여줄 개수
    # 객체만 render하는거고 객체를 html에서 메소드를통해구현하는것

    
    # 이렇게 옵젝으로 설정안하고 속성안하면 html에서 다음으로 못넘어가기때문 
    # page1기본값을 page_obj에 넣음
    # page_obj= 10개중에 일단 get_page 초기값 1로 보여줌
    # 객체를 생성해서 데이터만 조회하도록 쿼리,즉 속성할당하기위해씀
    # 속성을 html에 적용하기위해 context에 전달
    
    
    
    # context={'question_list':question_list}
    

def detail(request,question_id):
    # 자료형만가져오는거고 실질적으로는 controlleㄱ에서 받아오는것
    question=get_object_or_404(Question,pk=question_id)
    question.content

    question.answer_set.count
    context={'question':question}
    return render(request,'pybo/question_detail.html',context)
