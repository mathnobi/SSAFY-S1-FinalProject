from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True, unique=True)   # 유저 아이디 (자동 생성)
    username = models.CharField(max_length=100, unique=True)    # 이름 (unique 추가)
    age = models.IntegerField(default=26)                       # 나이 (한나가 만 26이라 26로 설정)
    gender = models.TextField(default='남')                     # 성별 (남/여)   
    salary = models.IntegerField(default=0)                     # 월급 (월급 모르니 0)
    wealth = models.IntegerField(default=0)                     # 자산 (자산 모르니 0)
    debt = models.IntegerField(default=0)                       # 빚 (빚 모르니 0) 
    tendency = models.IntegerField(default=1)                   # 투자성향 (1: 고위험 고수익, 2: 중위험 중수익, 3: 저위험 저수익)
    email = models.EmailField(unique=True)                     # 이메일 (unique 추가)
    products = models.TextField(blank=True, null=True)          # 예금 상품들을 담을 필드

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # related_name 추가
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # related_name 추가
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field, user_username
class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data

        email = data.get("email")
        username = data.get("username")
        age = data.get("age", None)
        gender = data.get("gender", None)
        salary = data.get("salary", None)
        wealth = data.get("wealth", None)
        debt = data.get("debt", None)
        tendency = data.get("tendency", None)

        if email:
            user_email(user, email)
        if username:
            user_username(user, username)

        if age is not None:
            user.age = age  
        if gender:
            user.gender = gender
        if salary is not None:
            user.salary = salary
        if wealth is not None:
            user.wealth = wealth
        if debt is not None:
            user.debt = debt
        if tendency is not None:
            user.tendency = tendency

        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()

        self.populate_username(request, user)
        if commit:
            user.save()

        return user
