from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
# Create your views here.
from .models import *
from .serializers import *
import requests
from django.http import HttpResponse


class CharacterView(ModelViewSet):

    pagination_class = None

    queryset = Character.objects.all().order_by('id')
    serializer_class = CharacterSerializers

# MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa


def Characterload(request):

    test = requests.get(
        'https://open-api.bser.io/v1/data/Character',
        headers={'x-api-key':'MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa'}
    )
    test_json = test.json()
    chlist = test_json['data']

    for i in chlist:
        try:
            tester_name = Character.objects.get(name=i['name'])
            continue

        except:

            Character(
                name = i['name'],
                attack = i['attackPower'],
                hp = i['maxHp'],
                hpregen = i['hpRegen'],
                stamina = i['maxSp'],
                stregen = i['spRegen'],
                defense = i['defense'],
                atkspeed = i['attackSpeed'],
                speed = i['moveSpeed'],
            ).save()


    return HttpResponse(chlist)