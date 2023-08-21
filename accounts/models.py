from django.db import models
from django.contrib.auth.models import *

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password = None, **extra_fields):

        if email is None:
            raise TypeError("이메일을 입력해주세요")
        
        if password is None:
            raise TypeError("비밀번호를 입력해주세요")
        
        user = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)

        user.save()

        return user
    
    def create_superuser(self,email,password,**extra_fields):

        if password is None:
            raise TypeError("비밀번호를 입력해주세요")
        
        user = self.create_user(email,password,**extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
    
team_list = (
        ('경영팀','경영팀'),
        ('고객대응팀','고객대응팀'),
        ('기술지원팀','기술지원팀'),
        ('전략기획팀','전략기획팀'),
        ('소속없음','소속없음'),
    )


class USER(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = None
    nickname = models.CharField(max_length=80, blank=True)
    email = models.EmailField(verbose_name="email", max_length=255, unique=True)
    realname = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    team = models.CharField(max_length=80, choices=team_list, default='소속없음')
    
    def __str__(self):
        return self.email
    
