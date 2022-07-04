from rest_framework import serializers

from article.models import Article as ArticleModel
from article.models import Comment as CommentModel


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
    
    class Meta:
        model = CommentModel
        fields = "__all__"

class ArticleSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True, source="comment_set")
    
    class Meta:
        model = ArticleModel
        # fields = ["content", "result_img"]
        fields = "__all__"
