from rest_framework import serializers
from .models import *
from accounts.models import *

class ArticleSerializer(serializers.ModelSerializer):


    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'create_user',
            'created_at',
            'updated_at',
            'hits',
            'subject',
        ]

