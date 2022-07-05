
from rest_framework import serializers

from user.models import User as UserModel
from article.models import Article as ArticleModel
from article.models import Comment as CommentModel
from django.db.models import F


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["username", "password"]

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user

    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user
