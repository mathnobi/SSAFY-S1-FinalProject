from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField()
    gender = serializers.CharField(max_length=10)
    salary = serializers.IntegerField()
    wealth = serializers.IntegerField()
    debt = serializers.IntegerField()
    tendency = serializers.IntegerField()
    email = serializers.EmailField(required=True)
    products = serializers.CharField(required=False, allow_blank=True)  

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'age': self.validated_data.get('age', ''),
            'gender': self.validated_data.get('gender', ''),
            'salary': self.validated_data.get('salary', ''),
            'wealth': self.validated_data.get('wealth', ''),
            'debt': self.validated_data.get('debt', ''),
            'tendency': self.validated_data.get('tendency', ''),
            'products': self.validated_data.get('products', ''),  
        }

class UserDetailsSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_username(username):
        if 'allauth.account' not in settings.INSTALLED_APPS:
            return username
        from allauth.account.adapter import get_adapter
        username = get_adapter().clean_username(username)
        return username

    class Meta:
        extra_fields = []
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'age'):
            extra_fields.append('age')
        if hasattr(UserModel, 'gender'):
            extra_fields.append('gender')
        if hasattr(UserModel, 'salary'):
            extra_fields.append('salary')
        if hasattr(UserModel, 'wealth'):
            extra_fields.append('wealth')
        if hasattr(UserModel, 'debt'):
            extra_fields.append('debt')
        if hasattr(UserModel, 'tendency'):
            extra_fields.append('tendency')
        if hasattr(UserModel, 'products'):  # 추가
            extra_fields.append('products')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        extra_fields = []
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'age'):
            extra_fields.append('age')
        if hasattr(UserModel, 'gender'):
            extra_fields.append('gender')
        if hasattr(UserModel, 'salary'):
            extra_fields.append('salary')
        if hasattr(UserModel, 'wealth'):
            extra_fields.append('wealth')
        if hasattr(UserModel, 'debt'):
            extra_fields.append('debt')
        if hasattr(UserModel, 'tendency'):
            extra_fields.append('tendency')
        if hasattr(UserModel, 'products'):  # 추가
            extra_fields.append('products')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)