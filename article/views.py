from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import viewsets, status, generics, mixins, filters
# Create your views here.
import datetime
from django.utils import timezone
from .permissions import *
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

class ArticleView(viewsets.ModelViewSet):

    queryset = Article.objects.all().order_by('-pk')
    serializer_class = ArticleSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ('title', 'createuser__nickname', 'subject', 'content')
    search_fields = ('title', 'createuser__nickname', 'content')

    def perform_create(self, serializer):

        serializer.save(
            createuser = self.request.user
        )

    def retrieve(self, request, pk=None, *args, **kwargs):
        # 조회수
        instance = get_object_or_404(self.get_queryset(),pk=pk)
        instance.hits_field +=1
        instance.save()
        
        return super().retrieve(request, *args, **kwargs)
    

class MyArticleView(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Article.objects.filter(createuser=user)
        else:
            return Article.objects.none()



class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('-pk')

    def perform_create(self, serializer):

        serializer.save(
            createuser=self.request.user,
            article=Article.objects.get(pk=self.kwargs.get("article_pk")),
        )


class LikeArticleView(viewsets.ModelViewSet):
    
    serializer_class = LikeArticleSerializer

    def get_queryset(self):
        article = Article.objects.get(pk=self.kwargs.get('pk'))
        
        return LikeArticle.objects.filter(article = article)
    
    def perform_create(self, serializer):
        article = Article.objects.get(pk=self.kwargs.get("pk"))
        like = LikeArticle.objects.filter(user=self.request.user, article = article)
        if like.exists():
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer.save(
            user=self.request.user,
            article=Article.objects.get(pk=self.kwargs.get("pk")),
        )


class BestArticleView(viewsets.ModelViewSet):

    serializer_class = ArticleSerializer

    queryset = Article.objects.annotate(count=Count('article_name')).filter(count__gt=30).order_by('-count')

