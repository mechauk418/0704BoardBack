from django.shortcuts import render
from .serializers import *
from .models import *
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# Create your views here.


class UserViewSet(ModelViewSet):

    queryset = USER.objects.all()
    serializer_class = UserSerializer
