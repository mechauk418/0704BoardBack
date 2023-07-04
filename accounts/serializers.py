from rest_framework import serializers
from .models import USER
from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account.adapter import get_adapter
from dj_rest_auth.serializers import LoginSerializer

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style = {'input_type':'password'})
    password2 = serializers.CharField(style = {'input_type':'password'})

    class Meta:
        model = USER
        fields = ['email','nickname','realname','password','password2']
        extra_kwargs = {
            'password': {
                'write_only':True
            }
        }

    def save(self,request):
        user = USER(
            email = self.validated_data['email'],
            nickname = self.validated_data['nickname'],
            realname = self.validated_data['realname'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'비밀번호가 틀립니다.'})
        
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = USER
        fields = ['id','email','nickname','realname']


class CSLoginSerializer(LoginSerializer):
    email = serializers.CharField(required = True, allow_blank = False)
    password = serializers.CharField(style = {'input_type':'password'})
    
