from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views

app_name = 'common'

urlpatterns = [
    # AuthenticationForm을 기본뷰로 사용자동생성 loginview는 그럼
    # 자동으로 template_name에 form context르르 추가해줌
    
    path('login/',auth_views.LoginView.as_view(template_name='common/login.html'),name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('signup/',views.singup,name='signup'),
]