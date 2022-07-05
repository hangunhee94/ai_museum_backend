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
    
    def validate(self, data):
        return data

    def create(self, validated_data):
        article = ArticleModel(**validated_data)
        article.save()
        return article

    # def update(self, instance, validated_data):
    #     print(validated_data)
    #     instance.content = validated_data['content']
    #     print(instance.content)
    #     instance.save()
    #     return instance

    class Meta:
        model = ArticleModel
        # fields = ["content", "image"]
        fields = "__all__"
