from django.contrib.auth.models import User
from django.db import models


# 모델에 추가할때마다 MIGRATE하기
# Create your models here.
class Question(models.Model):
    # 다대다는 중간테이블을 사용해서 두모델간의 관계를 관리하므로 on_delete가 의미가없음
    # on_dleete는 foreieng이나 onetoonefiled에서만관리
    voter=models.ManyToManyField(User,related_name='voter_question')
    # 각각 다르게  question을 여러개 가질수있기때문에 voter 1개가 Quesiton다를 가진다는것
    # 한마디로 voter가 여러개의 값을 가진다는것이다 1=여러개값을 가지는거고 다가 1개임
    
    # 역참조를통해서이제 user.voter_question가능 저거정안정하면 자동으로 question_set이되는데
    # 이럴경우 voter랑 author 모두 question_set으로 해당하기떄문에 어떤 필드로부터 역참조할지 알수가없음
    # voter로부터의 역참조,author로부터의 역참조는 각각 다 다름 한마디로 voter에 
    # voter의 question와 author 의 qeustion 은 다를수있따
    # voter의 question 역참조값과 author의 question 역참조는 다를 수있음
    # 각각 다른 집합을 가지는거니까 주의 각각의 필드는 다른 값을 가질수있따 주의
    
    # 필드들은 일단 다 1 Question 다
    # realated name을 사용안할시 modelname_set 예시: question_set으로 사용함
    # 또는 동일한 두모델간에 여러관계가있으면 각 관계 구분가능
    # Question에는 author과 voter라는 두개의 User관계가있기때문에
    # Question:User=다:1인데 필드는 author과 voter두개가 되어있어서
    # 어느필드로부터 역참조를할지 모르니까 결정해줘야함
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='author_question')
    # 모델의 메서드 foreingeky,CASECADE on_dleete는 옵션 kwargs**
    modify_date=models.DateTimeField(null=True,blank=True)
    subject=models.CharField(max_length=200)
    content=models.TextField()
    create_date=models.DateTimeField()
    def __str__(self):
        return self.subject
class Answer(models.Model):
    voter=models.ManyToManyField(User,related_name='author_answer')
    # Answer이 다 question이 1
    author=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='voter_answer')
    modify_date=models.DateTimeField(null=True,blank=True)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    content=models.TextField()
    create_date=models.DateTimeField()