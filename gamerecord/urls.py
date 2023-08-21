from django.urls import path, include
from .views import *

app_name = "gamerecord"


urlpatterns = [
    path("rererererer/", RecordView.as_view({'post':'create'})),
    path("getusernum/<str:nickname>/", getusernum)
]