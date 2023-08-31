from django.shortcuts import render, get_list_or_404
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
# Create your views here.
import requests
from django.http import JsonResponse, HttpResponse
import time
from rest_framework.response import Response
from datetime import datetime, timedelta, date
from rest_framework.pagination import PageNumberPagination
from collections import defaultdict
from character.models import Character

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

    now_time = datetime.now()


    # 가져온 전적을 등록하는 과정
    for game in matchdetail:
        time.sleep(2)
        print(game['gameId'])
        t = game['startDtm']
        gametime = datetime(int(t[0:4]),int(t[5:7]),int(t[8:10]), int(t[11:13]), int(t[14:16]), int(t[17:19])  )

        if len(Record.objects.filter(gamenumber = game['gameId'])):
        
            continue

        elif game['matchingMode'] !=3:

            continue

        elif (now_time - gametime).days >= 7:
            break

        else:

            gamepost = requests.get(
                f'https://open-api.bser.io/v1/games/{game["gameId"]}',
                headers={'x-api-key':'MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa'}
            )
            gamepost = gamepost.json()
            time.sleep(2)

            for g in gamepost['userGames']:
                if g['matchingMode'] !=3:
                    continue

                print(g['userNum'])
                print(g['nickname'])

                try:
                    temt = Gameuser.objects.get(nickname = g['nickname'])
                    gameid = Record.objects.create(
                        gamenumber = game['gameId'],
                        user = temt,
                        character = g['characterNum'],
                        beforemmr = g['mmrBefore'],
                        aftermmr = g['mmrAfter'],
                        gamerank = g['gameRank'],
                        playerkill = g['playerKill'],
                        playerAss = g['playerAssistant'],
                        mosterkill = g['monsterKill'],
                        startDtm = g['startDtm'],
                        mmrGain = g['mmrGain']
                    )

                except:
                        time.sleep(2)
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
                            character = g['characterNum'],
                            beforemmr = g['mmrBefore'],
                            aftermmr = g['mmrAfter'],
                            gamerank = g['gameRank'],
                            playerkill = g['playerKill'],
                            playerAss = g['playerAssistant'],
                            mosterkill = g['monsterKill'],
                            startDtm = g['startDtm'],
                            mmrGain = g['mmrGain']
                        )


    if 'next' in match:
        next_number = match['next']

        while True:

            days_check = False

            match = requests.get(
                f'https://open-api.bser.io/v1/user/games/{userNum}?next={next_number}',
                headers={'x-api-key':'MjckFi8vOaRRaueHKTRZ19X6ewJYfVf1WEkzTMZa'}
            )
            match = match.json()
            matchdetail = match['userGames']

            # 가져온 전적을 등록하는 과정
            for game in matchdetail:
                time.sleep(2)
                print(game['gameId'])
                t = game['startDtm']
                gametime = datetime(int(t[0:4]),int(t[5:7]),int(t[8:10]), int(t[11:13]), int(t[14:16]), int(t[17:19])  )

                if len(Record.objects.filter(gamenumber = game['gameId'])):
                
                    continue

                elif game['matchingMode'] !=3:
                    continue

                elif (now_time - gametime).days >= 7:
                    days_check = True
                    break

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
                        if g['matchingMode'] ==2:
                            continue

                        print(g['userNum'])
                        print(g['nickname'])

                        try:
                            temt = Gameuser.objects.get(nickname = g['nickname'])
                            gameid = Record.objects.create(
                                gamenumber = game['gameId'],
                                user = temt,
                                character = g['characterNum'],
                                beforemmr = g['mmrBefore'],
                                aftermmr = g['mmrAfter'],
                                gamerank = g['gameRank'],
                                playerkill = g['playerKill'],
                                playerAss = g['playerAssistant'],
                                mosterkill = g['monsterKill'],
                                startDtm = g['startDtm'],
                                mmrGain = g['mmrGain']
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
                                    character = g['characterNum'],
                                    beforemmr = g['mmrBefore'],
                                    aftermmr = g['mmrAfter'],
                                    gamerank = g['gameRank'],
                                    playerkill = g['playerKill'],
                                    playerAss = g['playerAssistant'],
                                    mosterkill = g['monsterKill'],
                                    startDtm = g['startDtm'],
                                    mmrGain = g['mmrGain']
                                )

            # 7일이 넘은 기록부터는 가져오지 않음
            if days_check:
                break

            if 'next' in match:
                next_number = match['next']
            else:
                break


    return JsonResponse(test_json)


def getuserRecord(request):

    

    return

class RecordPage(PageNumberPagination):
    page_size = 10


class RecordView(ModelViewSet):
    pagination_class = RecordPage

    def get_queryset(self, *args,**kwargs):
        print(self.kwargs.get('nickname'))
        usnum = Gameuser.objects.get(nickname = self.kwargs.get('nickname'))

        qs = Record.objects.filter(user=usnum)

        return qs

    serializer_class = RecordSerializer






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


class UserDetailView(ModelViewSet):

    queryset = Gameuser.objects.all()
    serializer_class = GameuserSerializer
    lookup_field = 'nickname'



def recentgainrp(request,nickname):
    
    ch_dict = defaultdict(int)
    ch_list = []
    userid = Gameuser.objects.get(nickname = nickname)
    userrecord = Record.objects.filter(user = userid, startDtm__range=[date.today()-timedelta(days=3),date.today()])

    for g in userrecord:
        chname = Character.objects.get(id=g.character).name
        ch_dict[chname]+=g.mmrGain

    print(ch_dict)

    return JsonResponse(ch_dict)

