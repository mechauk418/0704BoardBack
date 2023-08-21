from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.decorators import method_decorator
# Create your views here.
from rest_framework.response import Response
import requests
from rest_framework.throttling import UserRateThrottle
from rest_framework.throttling import BaseThrottle
from rest_framework import versioning, filters
import django_filters.rest_framework
from rest_framework import exceptions, status

# class TestThrottle(BaseThrottle):
#     scope = 'anon'
#     def allow_request(self, request, view):
#         if request.method == 'GET':
#             return True
#         if request.method == 'POST':
#             return False
#         return super().allow_request(request, view)


class Task_ViewSet(ModelViewSet):
    
    queryset = Task.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    # throttle_classes = [TestThrottle]
    filter_backends = [filters.SearchFilter]
    search_fields  = ['title','content','subtasks__team']

    def perform_create(self, serializer):
        
        serializer.save(
            create_user = self.request.user.realname
        )


class SubTask_ViewSet(ModelViewSet):

    serializer_class = SubTaskSerializer

    def perform_create(self, serializer):
        serializer.save(
            task = Task.objects.get(id=self.kwargs.get('Task_id')),
        )
    
    def get_queryset(self):
        
        return SubTask.objects.filter(task=self.kwargs.get('Task_id'))

    def destroy(self, request, *args, **kwargs):
        
        complete_check = self.get_object()
        if complete_check.is_complete:
            raise exceptions.ValidationError("완료된 하위 업무는 삭제할 수 없습니다.")
        
        else:
            return super().destroy(request, *args, **kwargs)
        
    def perform_update(self, serializer):
        print(self.kwargs.get('pk'))
        subpk = self.kwargs.get('pk')
        task = Task.objects.get(id=self.kwargs.get('Task_id'))
        root = task.subtasks.all()
        if 'is_complete' in self.request.data:
            checkdata = self.request.data['is_complete']
        else:
            checkdata = False

        remain = task.subtasks.exclude(id=subpk)
        
        alltruecheck = True

        for r in remain:
            if not r.is_complete:
                alltruecheck = False

        if checkdata and alltruecheck:
            task.is_complete = True
            task.save()
        else:
            task.is_complete = False
            task.save()

        if checkdata:
            if self.request.user.team != self.request.data['team']:
                raise exceptions.ValidationError('두개가 다름')

        return super().perform_update(serializer)
