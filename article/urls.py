from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'articles'

router = DefaultRouter()
router.register('', views.ArticleView)

urlpatterns =[
    path('', include(router.urls)),
    path("<int:article_pk>/comment/", views.CommentView.as_view({"post": "create", "get": "list"})),
    path("<int:article_pk>/comment/<int:pk>/", views.CommentView.as_view({'get':'retrieve', "delete": "destroy", "put": "update", "patch": "partial_update"})),
]