from django.urls import path, include
from .views import *

app_name = "todo"

urlpatterns = [
    path("", Task_ViewSet.as_view({'get':'list', 'post':'create'})),
    path("<int:pk>/", Task_ViewSet.as_view({'get':'retrieve', "delete": "destroy", "put": "update", "patch": "partial_update"})),
    path("<int:Task_id>/SubTask/", SubTask_ViewSet.as_view({'get':'list', 'post':'create'})),
    path("<int:Task_id>/SubTask/<int:pk>/", SubTask_ViewSet.as_view({"put": "update", "patch": "partial_update", "delete": "destroy", "get": 'retrieve'})),
]