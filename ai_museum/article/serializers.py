from rest_framework import serializers

from article.models import Article as ArticleModel
from article.models import Comment as CommentModel


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
    
    class Meta:
        model = CommentModel
        fields = ["user", "contents"]

class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, source="comments_set")
    
    class Meta:
        model = ArticleModel
        fields = ["content", "comments"]