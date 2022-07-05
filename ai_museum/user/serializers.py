from rest_framework import serializers

from article.models import Article as ArticleModel
from article.models import Comment as CommentModel

from user.models import User as UserModel
from article.serializers import ArticleSerializer
from user.models import User as UserModel

class UserSignupSerializer(serializers.ModelSerializer):

    # 기존 함수를 덮어씀
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()

        return user
    class Meta:
                # serializer에 사용될 model, field지정
        model = UserModel
                # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용
        fields = ["username", "password"]
                  

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = "__all__"

