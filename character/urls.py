from django.urls import path, include
from .views import *


urlpatterns = [
    path("", CharacterView.as_view({'get':'list', 'post':'create'})),
    path("load/", Characterload)
]