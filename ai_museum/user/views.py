from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from django.contrib.auth import login, logout, authenticate

from ai_museum.permissions import IsAdminOrIsAuthenticatedReadOnly

from user.serializers import UserSerializer, UserSignupSerializer

# 사용자에게 토큰을 할당하기 위한 구성
from user.jwt_claim_serializer import SpartaTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserView(APIView):
    permission_classes =[permissions.AllowAny]
    # permission_classes = [IsAdminOrIsAuthenticatedReadOnly]
    # permission_classes = [permissions.IsAuthenticated]

    # 사용자 정보 조회
    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    # 회원가입
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입 완료"})
        else:
            print(serializer.errors)
            return Response({"message": "가입 실패"})

    # 회원 정보 수정
    def put(self, request):
        return Response({"message": "put method!!"})

    # 회원 탈퇴
    def delete(self, request):
        return Response({"message": "delete method!!"})


# 토큰 할당
class SpartaTokenObtainPairView(TokenObtainPairView):
    serializer_class = SpartaTokenObtainPairSerializer