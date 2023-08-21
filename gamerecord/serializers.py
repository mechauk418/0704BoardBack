
from .models import *
from rest_framework.serializers import ModelSerializer

class RecordSerializer(ModelSerializer):

    class Meta:
        model = record
        fields = '__all__'     
