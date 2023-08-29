
from .models import *
from rest_framework import serializers


class GameDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Record
        fields = '__all__'


class GameuserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gameuser
        fields = '__all__'

class RecordSerializer(serializers.ModelSerializer):

    gamedetail = serializers.SerializerMethodField()

    nowuserstats = serializers.SerializerMethodField()

    def get_gamedetail(self,obj):
        data = Record.objects.filter(gamenumber = obj.gamenumber)

        return GameDetailSerializer(instance=data, many=True, context = self.context).data

    def get_nowuserstats(self,obj):

        data = Gameuser.objects.filter(nickname = obj.user.nickname)
        print('data',data)

        return GameuserSerializer(instance=data, many=True, context = self.context).data


    class Meta:
        model = Record
        fields = '__all__'

