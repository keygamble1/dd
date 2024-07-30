from django.apps import AppConfig


class PyboConfig(AppConfig):
    # model의 field를 자동하려면 app에 넣어야함 pyboconfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pybo'
