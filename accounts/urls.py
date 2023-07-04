from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path("", UserViewSet.as_view({'get':'list', "post":'create'})),
    path("<int:pk>/", UserViewSet.as_view({'get':'retrieve', "delete": "destroy", "put": "update", "patch": "partial_update"})),
]
