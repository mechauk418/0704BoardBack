
from .models import *
from rest_framework import serializers
from character.models import Character

class GameDetailSerializer(serializers.ModelSerializer):


    playcharacter = serializers.SerializerMethodField()

    def get_playcharacter(self,obj):
        ch = Character.objects.get(id=obj.character)
        
        return ch.name
    
    usernickname = serializers.SerializerMethodField()


    def get_usernickname(self,obj):
        nick = Gameuser.objects.get(id=obj.user.id)
        
        return nick.nickname

    class Meta:
        model = Record
        fields = '__all__'


class GameuserSerializer(serializers.ModelSerializer):

    averageDamage = serializers.SerializerMethodField()

    def get_averageDamage(self,obj):

        games = Record.objects.filter(user = obj)
        sumDamage = 0
        for game in games:
            sumDamage += game.damageToPlayer

        avgD = int(sumDamage/len(games))

        
        return avgD


    class Meta:
        model = Gameuser
        fields = '__all__'

class RecordSerializer(serializers.ModelSerializer):

    gamedetail = serializers.SerializerMethodField()
    
    playcharacter = serializers.SerializerMethodField()

    def get_playcharacter(self,obj):
        ch = Character.objects.get(id=obj.character)
        
        return ch.name

    def get_gamedetail(self,obj):
        data = Record.objects.filter(gamenumber = obj.gamenumber).order_by('gamerank')

        return GameDetailSerializer(instance=data, many=True, context = self.context).data

    usernickname = serializers.SerializerMethodField()


    def get_usernickname(self,obj):
        nick = Gameuser.objects.get(id=obj.user.id)
        
        return nick.nickname


    class Meta:
        model = Record
        fields = '__all__'


class UserUseSerializer(serializers.ModelSerializer):

    usech = serializers.SerializerMethodField()

    def get_usech(self,obj):
        userlist = []
        checklist = [] # 중복 체크
        qs = Record.objects.filter(user = obj).order_by('character')
        for i in qs:
            temt = Character.objects.get(id=i.character)
            if temt.pk not in checklist:
                checklist.append(temt.pk)
                userlist.append( {'chname': temt.koreanname, 'chnumber':temt.pk} )

            else:
                continue

                

        return userlist

    class Meta:
        model = Gameuser
        fields = ['usech']