from rest_framework import serializers

from article.models import Article as ArticleModel
# from article.models import Comment as CommentModel


# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()
    
#     def get_user(self, obj):
#         return obj.user.username
    
    # class Meta:
    #     model = CommentModel
    #     fields = "__all__"

# class ArticleImageModel(serializers.ModelSerializer):
#     def get_user(self, obj):
#         return obj.user.username

#     class Meta:
#         model = ArticleImageModel
#         fields = "__all__"

class ArticleSerializer(serializers.ModelSerializer):

    # number = serializers.SerializerMethodField()  # 1. 필드 추가

    # def get_first_name(self, obj):  # 2. 메소드 추가. 이 메소드는 객체를 인자로 받고
    #     return obj.full_name['number']  # 객체의 full_name 속성 값에서 'last_name' 키 값을 리턴

    class Meta:
        model = ArticleModel
        # fields = ["user", "content", "image"]
        fields = "__all__"

    # comments = CommentSerializer(many=True, source="comment_set")
    
    # def validate(self, data):
    #     return data

    # def create(self, validated_data):
    #     article = ArticleModel(**validated_data)
    #     article.save()
    #     return article

    # def update(self, instance, validated_data):
    #     print(validated_data)
    #     instance.content = validated_data['content']
    #     print(instance.content)
    #     instance.save()
    #     return instance