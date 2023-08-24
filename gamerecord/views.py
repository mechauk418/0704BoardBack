from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
# Create your views here.
import requests
from django.http import JsonResponse, HttpResponse
import time

def getusernum(request,nickname):

    # 유저 닉네임으로 유저 정보 받아옴
    print(nickname)
    userNum = requests.get(
        f'https://open-api.bser.io/v1/user/nickname?query={nickname}',
        headers={'x-api-key':'MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa'}
    )
    test_json = userNum.json()
    userNum = test_json['user']['userNum']
    
    print(userNum) 


    # 유저의 이번 시즌 정보를 받아옴, 19는 정규시즌1 번호
    userstats = requests.get(
        f'https://open-api.bser.io/v1/user/stats/{userNum}/19',
        headers={'x-api-key':'MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa'}
    ).json()['userStats'][0]

    # 처음 검색해서 DB에 유저가 없음
    if not Gameuser.objects.filter(nickname = userstats['nickname']):
        Gameuser.objects.create(
            userNum = userstats['userNum'],
            mmr = userstats['mmr'],
            nickname = userstats['nickname'],
            rank = userstats['rank'],
            totalGames = userstats['totalGames'],
            winrate = round((userstats['totalWins']*100 / userstats['totalGames']),1),
            averageKills = userstats['averageKills'],
        )
        

    # 유저 넘버로 유저의 최근 90일 내의 전적을 모두 가져옴
    match = requests.get(
        f'https://open-api.bser.io/v1/user/games/{userNum}',
        headers={'x-api-key':'MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa'}
    )
    match = match.json()
    matchdetail = match['userGames']



    for game in matchdetail:
        time.sleep(3)
        print(game['gameId'])

        if len(Record.objects.filter(gamenumber = game['gameId'])):
        
            continue

        else:
            print('except')

            gamepost = requests.get(
                f'https://open-api.bser.io/v1/games/{game["gameId"]}',
                headers={'x-api-key':'MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa'}
            )
            gamepost = gamepost.json()
            time.sleep(2)
            print(gamepost)

            for g in gamepost['userGames']:
                time.sleep(2)

                print(g['userNum'])
                print(g['nickname'])

                try:
                    temt = Gameuser.objects.get(nickname = g['nickname'])
                    gameid = Record.objects.create(
                        gamenumber = game['gameId'],
                        user = temt,
                        character = game['characterNum'],
                        beforemmr = game['mmrBefore'],
                        aftermmr = game['mmrAfter'],
                        gamerank = game['gameRank'],
                        playerkill = game['playerKill'],
                        playerAss = game['playerAssistant'],
                        mosterkill = game['monsterKill']
                    )

                except:
                        time.sleep(1)
                        anotheruser = requests.get(
                            f'https://open-api.bser.io/v1/user/stats/{g["userNum"]}/19',
                            headers={'x-api-key':'MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa'}
                        ).json()['userStats'][0]

                        temt = Gameuser.objects.create(
                            userNum = anotheruser['userNum'],
                            mmr = anotheruser['mmr'],
                            nickname = anotheruser['nickname'],
                            rank = anotheruser['rank'],
                            totalGames = anotheruser['totalGames'],
                            winrate = round((anotheruser['totalWins']*100 / anotheruser['totalGames']),1),
                            averageKills = anotheruser['averageKills'],
                        )
                        gameid = Record.objects.create(
                            gamenumber = game['gameId'],
                            user = temt,
                            character = game['characterNum'],
                            beforemmr = game['mmrBefore'],
                            aftermmr = game['mmrAfter'],
                            gamerank = game['gameRank'],
                            playerkill = game['playerKill'],
                            playerAss = game['playerAssistant'],
                            mosterkill = game['monsterKill']
                        )



    return JsonResponse(gamepost)

def getuserRecord(request):

    

    return


class RecordView(ModelViewSet):

    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)



def refreshuser(request,nickname):

    userNum = requests.get(
        f'https://open-api.bser.io/v1/user/nickname?query={nickname}',
        headers={'x-api-key':'MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa'}
    )
    test_json = userNum.json()
    userNum = test_json['user']['userNum']
    
    print(userNum) # 유저 닉네임으로 유저 정보 받아옴

    userstats = requests.get(
        f'https://open-api.bser.io/v1/user/stats/{userNum}/19',
        headers={'x-api-key':'MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa'}
    ).json()['userStats'][0]
    print(userstats)

    Gameuser.objects.update(
        userNum = userstats['userNum'],
        mmr = userstats['mmr'],
        nickname = userstats['nickname'],
        rank = userstats['rank'],
        totalGames = userstats['totalGames'],
        winrate = round((userstats['totalWins']*100 / userstats['totalGames']),1),
        averageKills = userstats['averageKills'],
    )