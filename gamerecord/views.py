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
from django.utils import timezone
import json


# 현재 한국 시간 aware 설정
now_time = timezone.localtime(timezone.now())


def refreshuser(nickname):
    time.sleep(0.02)
    userNum = requests.get(
        f'https://open-api.bser.io/v1/user/nickname?query={nickname}',
        headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}
    )
    test_json = userNum.json()
    userNum = test_json['user']['userNum']
    
    print(userNum) # 유저 닉네임으로 유저 정보 받아옴
    time.sleep(0.02)
    userstats = requests.get(
        f'https://open-api.bser.io/v1/user/stats/{userNum}/19',
        headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}
    ).json()['userStats'][0]

    te = Gameuser.objects.get(userNum = userstats['userNum'])
    te.mmr = userstats['mmr']
    te.rank = userstats['rank']
    te.totalGames = userstats['totalGames']
    te.winrate = round((userstats['totalWins']*100 / userstats['totalGames']),1)
    te.averageKills = userstats['averageKills']
    te.save()

    return JsonResponse(test_json)


def getusernum(nickname):
    sttime = time.time()
    # 유저 닉네임으로 유저 정보 받아옴
    print(nickname)
    time.sleep(0.02)
    userNum = requests.get(
        f'https://open-api.bser.io/v1/user/nickname?query={nickname}',
        headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}
    )
    test_json = userNum.json()
    userNum = test_json['user']['userNum']
    
    print(userNum)
    

    # 유저의 이번 시즌 정보를 받아옴, 19는 정규시즌1 번호
    time.sleep(0.02)
    userstats = requests.get(
        f'https://open-api.bser.io/v1/user/stats/{userNum}/19',
        headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}
    ).json()['userStats'][0]

    # 처음 검색해서 DB에 유저가 없음
    if not Gameuser.objects.filter(nickname = userstats['nickname']):
        utc_ = timedelta(hours=9)
        Gameuser.objects.create(
            userNum = userstats['userNum'],
            mmr = userstats['mmr'],
            nickname = userstats['nickname'],
            rank = userstats['rank'],
            totalGames = userstats['totalGames'],
            winrate = round((userstats['totalWins']*100 / userstats['totalGames']),1),
            averageKills = userstats['averageKills'],
        )
    
    refreshuser(nickname)

    search_user = Gameuser.objects.get(nickname = nickname)

    # 유저 넘버로 유저의 최근 90일 내의 전적을 모두 가져옴
    time.sleep(0.02)
    match = requests.get(
        f'https://open-api.bser.io/v1/user/games/{userNum}',
        headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}
    ).json()
    matchdetail = match['userGames']
    
    # 가져온 전적을 등록하는 과정
    for game in matchdetail:
        print(game['gameId'])
        t = game['startDtm']
        gametime = datetime(int(t[0:4]),int(t[5:7]),int(t[8:10]), int(t[11:13]), int(t[14:16]), int(t[17:19]))
        gametime_aware = timezone.make_aware(gametime)
        if len(Record.objects.filter(gamenumber = game['gameId'])):
        
            continue

        elif game['matchingMode'] !=3:

            continue

        elif (now_time - gametime_aware).days >= 14:
            break

        else:
            time.sleep(0.02)
            gamepost = requests.get(
                f'https://open-api.bser.io/v1/games/{game["gameId"]}',
                headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}
            )
            gamepost = gamepost.json()
            # if 'userGames' not in gamepost:
            #                    gamepost = requests.get(
            #     f'https://open-api.bser.io/v1/games/{game["gameId"]}',
            #     headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}
            #     ).json()
            

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
                        mmrGain = g['mmrGain'],
                        damageToPlayer = g['damageToPlayer'],
                        damageToMonster  = g['damageToMonster'],
                        premaid  = g['preMade'],
                        useWard  = g['addSurveillanceCamera']+g['addTelephotoCamera'],
                        useConsole = g['useSecurityConsole'],
                    )

                except:
                    time.sleep(0.02)
                    anotheruser = requests.get(
                        f'https://open-api.bser.io/v1/user/stats/{g["userNum"]}/19',
                        headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}
                    ).json()
                    print(anotheruser)
                    # if 'userStats' not in anotheruser:
                    #                            anotheruser = requests.get(
                    #     f'https://open-api.bser.io/v1/user/stats/{g["userNum"]}/19',
                    #     headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}).json()
                    #     anotheruser = anotheruser['userStats'][0]
                    # else:
                    anotheruser = anotheruser['userStats'][0]

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
                        mmrGain = g['mmrGain'],
                        damageToPlayer = g['damageToPlayer'],
                        damageToMonster  = g['damageToMonster'],
                        premaid  = g['preMade'],
                        useWard  = g['addSurveillanceCamera']+g['addTelephotoCamera'],
                        useConsole = g['useSecurityConsole'],
                    )


    if 'next' in match:
        next_number = match['next']

        while True:

            days_check = False
            time.sleep(0.02)
            match = requests.get(
                f'https://open-api.bser.io/v1/user/games/{userNum}?next={next_number}',
                headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'})
            match = match.json()
            # while 'userGames' not in match:
            #     match = requests.get(
            #     f'https://open-api.bser.io/v1/user/games/{userNum}?next={next_number}',
            #     headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}).json()
            matchdetail = match['userGames']
            upt = matchdetail[0]['startDtm']
            test_time = datetime(int(upt[0:4]),int(upt[5:7]),int(upt[8:10]), int(upt[11:13]), int(upt[14:16]), int(upt[17:19])  )
            test_time_aware = timezone.make_aware(test_time)

            if search_user.updatedate is not None and \
                search_user.updatedate > test_time_aware:
                break


            # 가져온 전적을 등록하는 과정
            for game in matchdetail:
                
                print(game['gameId'])
                t = game['startDtm']
                gametime = datetime(int(t[0:4]),int(t[5:7]),int(t[8:10]), int(t[11:13]), int(t[14:16]), int(t[17:19])  )
                gametime_aware = timezone.make_aware(gametime)

                if len(Record.objects.filter(gamenumber = game['gameId'])):
                    
                    continue

                elif game['matchingMode'] !=3:
                    continue

                elif (now_time - gametime_aware).days >= 14:
                    days_check = True
                    break

                else:
                    print('except')
                    time.sleep(0.02)
                    gamepost = requests.get(
                        f'https://open-api.bser.io/v1/games/{game["gameId"]}',
                        headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}
                    )
                    gamepost = gamepost.json()
                    # while 'userGames' not in gamepost:
                    #                            gamepost = requests.get(
                    #     f'https://open-api.bser.io/v1/games/{game["gameId"]}',
                    #     headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}
                    #     ).json()

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
                                mmrGain = g['mmrGain'],
                                damageToPlayer = g['damageToPlayer'],
                                damageToMonster  = g['damageToMonster'],
                                premaid  = g['preMade'],
                                useWard  = g['addSurveillanceCamera']+g['addTelephotoCamera'],
                                useConsole = g['useSecurityConsole'],
                            )

                        except:
                            time.sleep(0.02)
                            anotheruser = requests.get(
                                f'https://open-api.bser.io/v1/user/stats/{g["userNum"]}/19',
                                headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}
                            ).json()

                            # while 'userStats' not in anotheruser:
                            #     print(anotheruser)
                            #     anotheruser = requests.get(
                            #     f'https://open-api.bser.io/v1/user/stats/{g["userNum"]}/19',
                            #     headers={'x-api-key':'alo3AXT2HC1SEa9MaVKOc10lHQ8LvYHr2SKf8zGU'}).json()
                            #     print(anotheruser)

                            anotheruser = anotheruser['userStats'][0]

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
                                mmrGain = g['mmrGain'],
                                damageToPlayer = g['damageToPlayer'],
                                damageToMonster  = g['damageToMonster'],
                                premaid  = g['preMade'],
                                useWard  = g['addSurveillanceCamera']+g['addTelephotoCamera'],
                                useConsole = g['useSecurityConsole'],
                            )

            # 7일이 넘은 기록부터는 가져오지 않음
            if days_check:
                break

            if 'next' in match:
                next_number = match['next']
            else:
                break

    edtime = time.time()
    print(f"{edtime - sttime:.5f} sec")
    search_user.updatedate = now_time
    search_user.save()

    return JsonResponse(test_json)


def getuserRecord(request):

    

    return

class RecordPage(PageNumberPagination):
    page_size = 10


class RecordView(ModelViewSet):
    pagination_class = RecordPage

    def get_queryset(self, *args,**kwargs):

        print(self.kwargs.get('nickname'))
        try:
            usnum = Gameuser.objects.get(nickname = self.kwargs.get('nickname'))
            # getusernum(self.kwargs.get('nickname'))
        except:
            getusernum(self.kwargs.get('nickname'))
            usnum = Gameuser.objects.get(nickname = self.kwargs.get('nickname'))

        qs = Record.objects.filter(user=usnum).order_by('-gamenumber')

        return qs
    
    def create(self, request, *args, **kwargs):
        getusernum(self.kwargs.get('nickname'))

        return
        

    serializer_class = RecordSerializer


class UserDetailView(ModelViewSet):

    queryset = Gameuser.objects.all()
    serializer_class = GameuserSerializer
    lookup_field = 'nickname'


def recentgainrp(request,nickname):
    
    alldict = dict()
    
    ch_dict = defaultdict(int)
    ch2_dict = defaultdict(int)

    userid = Gameuser.objects.get(nickname = nickname)
    userrecord = Record.objects.filter(user = userid, startDtm__range=[date.today()-timedelta(days=14),date.today()])

    for g in userrecord:
        chname = Character.objects.get(id=g.character).koreanname
        ch_dict[chname]+=g.mmrGain
        ch2_dict[chname]+=1

    ch2_item = list(ch2_dict.items())
    ch2_item.sort(key=lambda x:(-x[1]))

    print(ch2_item)
    result_list = []

    for item in ch2_item:
        temtdict = dict()
        temtdict['chname']=item[0]
        temtdict['trygame']=item[1]
        temtdict['mmrGain']=ch_dict[item[0]]
        result_list.append(temtdict)
        
    alldict['result'] = result_list
    print(alldict)

    return JsonResponse(alldict)


def testrp(request,nickname):

    return getusernum(nickname)