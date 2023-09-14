from rest_framework import serializers
from .models import Character



class CharacterSerializers(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = '__all__'


class CharacterRPSerializers(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = ['koreanname','trygame7days','RPfor7days' , 'RPeff',  ]