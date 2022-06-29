from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from article.models import Article as ArticleModel

from article.serializers import ArticleSerializer
from django.utils import timezone
# Create your views here.
class ArticleView(APIView):
    # 로그인 한 사용자의 게시글 목록 return
    permission_classes =[permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [IsAdminOrIsAuthenticatedReadOnly]

    def get(self, request):
        user = request.user
        today =timezone.now()

        articles = ArticleModel.objects.filter(
            exposure_start_date__lte = today,
            exposure_end_date__gte = today,    
        ).order_by("-id")

        serializer = ArticleSerializer(articles, many=True).data

        return Response(serializer, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        title = request.data.get("content","")
        # exposure_start_date =request.date.get("exposure_start_date")
        # exposure_end_date =request.date.get("exposure_end_date")
        

        if len(title) <= 5:
            return Response({"error": "내용은 5자 이상 작성해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        article = ArticleModel(
            user=user,
            **request.data
            # title=title,
            # contents=contents,
            # exposure_start_date=exposure_start_date,
            # exposure_end_date=exposure_end_date,
            )

        article.save()
        return Response({"message": "성공"}, status=status.HTTP_200_OK)