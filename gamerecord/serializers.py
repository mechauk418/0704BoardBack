
from .models import *
from rest_framework.serializers import ModelSerializer

class RecordSerializer(ModelSerializer):

    class Meta:
        model = Record
        fields = '__all__'     
