from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from common.forms import UserForm


# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('index')

def singup(request):
    if request.method == "POST":
        form=UserForm(request.POST)
        if form.is_valid():
            # 유효성 검사를 통과한 데이터에 접근
            form.save()
            # model form은 save해줘야함
            # save안하면 저장이안디ㅗㅁ
            username=form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=raw_password)
            # 자동인증
            login(request,user)
            return redirect('index')
            # request 클릭전 쓴 모든 이벤트
    else:
        form=UserForm()

    return render(request,'common/signup.html',{'form':form})