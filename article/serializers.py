from rest_framework import serializers
from .models import *
from accounts.models import *


class CommentSerializer(serializers.ModelSerializer):

    useremail = serializers.ReadOnlyField(source='create_user.email')
    userpk = serializers.ReadOnlyField(source ='create_user.id')

    class Meta:
        model = Comment
        fields = [
            'content',
            'create_user',
            'created_at',
            'article',
            'useremail',
            'userpk'
        ]

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

