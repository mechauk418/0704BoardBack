from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, status, generics, mixins
# Create your views here.

class ArticleView(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):

        serializer.save(
            create_user = self.request.user
        )

        return super().perform_create(serializer)