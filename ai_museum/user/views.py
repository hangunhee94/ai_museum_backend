from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from django.contrib.auth import login, logout, authenticate
from user.models import User as UserModel

from .serializer import UserSignupSerializer


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response()
    # 회원가입

    def post(self, request):
        data = request.data
        serializer = UserSignupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공"})
        else:
            print(serializer.errors)
            return Response({"message": "회원가입 실패"})

    # 회원 정보 수정
    def put(self, request):
        return Response({"message": "put method!!"})
    # 회원 탈퇴

    def delete(self, request):
        return Response({"message": "delete method!!"})


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    # 로그인

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."})
        login(request, user)

        return Response({"message": "login success!!"})
    # 로그아웃

    def delete(self, request):
        logout(request)
        return Response({"message": "logout success!!"})

# test


class TestView(APIView):
    def get(self, request):
        return Response({"message": "get ok!"})

    def post(self, request):
        return Response({"message": "post ok!"})

    def put(self, request):
        return Response({"message": "put ok!"})

    def delete(self, request):
        return Response({"message": "delete ok!"})
