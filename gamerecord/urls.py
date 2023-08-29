from django.urls import path, include
from .views import *

app_name = "gamerecord"


urlpatterns = [
    path("rererererer/", RecordView.as_view({'post':'create'})),
    path("getusernum/<str:nickname>/", getusernum),
    path("getsearch/<str:nickname>/", RecordView.as_view({'get':'list'})),
    path("getdetail/<str:nickname>/", UserDetailView.as_view({'get':'retrieve'})),
    path("getdetail/", UserDetailView.as_view({'get':'list'})),
]