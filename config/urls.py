"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from pybo.views import base_views

# 폴더안에 init__이있어야 인식을함
# /기본url 추가해줘ㅑ함 login redirect url추가했으면
# url패턴도추가해야하는것 패턴추가안하면 아무것도모름
urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/',include('pybo.urls')),    
    path('common/',include('common.urls')),
    path('',base_views.index,name='index'),
    # /할필요는 없다 ''=/기때문 /쓰면 //가됨
    # admin/도 /admin/이거라서  다른url도 /를 끝에다붙이는것
]
