from rest_framework import serializers

from article.models import Article as ArticleModel
from article.models import Comment as CommentModel

from user.models import User as UserModel

from article.serializers import ArticleSerializer, CommentSerializer



class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["username" , "password"]

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

    def update(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True, source = "article_set")
    comments = CommentSerializer(many=True, source = "comment_set")

    class Meta:
        model = UserModel
        fields = ["username", "email", "join_date", "articles", "comments"]