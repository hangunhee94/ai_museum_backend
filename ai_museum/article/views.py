from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from article.serializers import ArticleSerializer, CommentSerializer

from .models import Article as ArticleModel
from .models import Comment as CommentModel


class ArticleView(APIView):

    def get(self, request, article_id):
        article = ArticleModel.objects.filter(article=article_id)
        serialized_data = CommentSerializer(
            article, many=True).data  # queryset
        return Response(serialized_data, status=status.HTTP_200_OK)

    # 게시글 작성
    def post(self, request):
        request.data['artist'] = request.user.id
        print(f'리퀘스트 데이터 -> {request.data}')
        article_serializer = ArticleSerializer(data=request.data)

        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 수정
    def put(self, request, article_id):
        article = ArticleModel.objects.get(id=article_id)
        article_serializer = ArticleSerializer(
            article, data=request.data, partial=True)

        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제
    def delete(self, request):
        return Response({'message': '삭제 성공!'})


class CommentView(APIView):
    # 댓글 조회
    def get(self, request, article_id):
        comment = CommentModel.objects.filter(article=article_id)
        serialized_data = CommentSerializer(
            comment, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)

    # 댓글 작성
    def post(self, request, article_id):
        request.data["user"] = request.user.id
        request.data["article"] = article_id
        comment_serializer = CommentSerializer(data=request.data)

        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(comment_serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # 업데이트
    def put(self, request, comment_id):
        comment = CommentModel.objects.get(id=comment_id)
        comment_serializer = CommentSerializer(
            comment, data=request.data, partial=True)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(comment_serializer.error, status=status.HTTP_400_BAD_REQUEST)

    # 삭제
    def delete(self, request, comment_id):
        comment = CommentModel.objects.get(id=comment_id)
        comment.delete()
        return Response(status=status.HTTP_200_OK)


class LikeView(APIView):
    def post(self, request, article_id):
        user = request.user
        article = ArticleModel.objects.get(id=article_id)
        likes = article.likes.all()
        like_lists = []
        for like in likes:
            like_lists.append(like.id)

        if user.id in like_lists:
            article.likes.remove(user)
            return Response({'message': '취소'})
        else:
            article.likes.add(user)
            return Response({'message': '좋아요'})
