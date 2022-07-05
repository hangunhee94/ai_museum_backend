from rest_framework import serializers

from .models import Article as ArticleModel
from .models import Comment as CommentModel


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ArticleModel


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = CommentModel


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'likes'
        model = ArticleModel
