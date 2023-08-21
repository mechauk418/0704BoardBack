from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
# Create your views here.
import requests
from django.http import JsonResponse

def getusernum(request,nickname):
    print(nickname)
    userNum = requests.get(
        f'https://open-api.bser.io/v1/user/nickname?query={nickname}',
        headers={'x-api-key':'MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa'}
    )
    test_json = userNum.json()
    userNum = test_json['user']['userNum']
    
    print(userNum)

    match = requests.get(
        f'https://open-api.bser.io/v1/user/games/{userNum}',
        headers={'x-api-key':'MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa'}
    )
    match = match.json()
    matchdetail = match['userGames']
    

    return JsonResponse(match)

def getuserrecord(request):

    

    return


class RecordView(ModelViewSet):

    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)
