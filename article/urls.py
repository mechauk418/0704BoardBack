from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'articles'

urlpatterns =[
    path("<int:article_pk>/comment/", views.CommentView.as_view({"post": "create", "get": "list"})),
    path("<int:article_pk>/comment/<int:pk>/", views.CommentView.as_view({'get':'retrieve', "delete": "destroy", "put": "update", "patch": "partial_update"})),
    path('<int:pk>/like/',views.LikeArticleView.as_view({'get':'list', "post": "create"})), 
    path("", views.ArticleView.as_view({"post": "create", "get": "list"})),
    path("<int:pk>/", views.ArticleView.as_view({'get':'retrieve', "delete": "destroy", "put": "update", "patch": "partial_update"})),
    path("mypost/", views.MyArticleView.as_view({"get": "list"})),
    path("bestarticle/", views.BestArticleView.as_view({"post": "create", "get": "list"})),
]