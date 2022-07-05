from django.contrib.auth import login, authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.views.decorators.csrf import csrf_exempt
from user.serializers import UserSignupSerializer, UserSerializer


class UserView(APIView):
    # permission_classes = [permissions.AllowAny]       # 누구나 view 접근 가능
    # # permission_classes = [permissions.IsAuthenticated] # 로그인된 사용자만 view 접근 가능
    # # permission_classes = [permissions.IsAdminUser]     # admin 유저만 view 접근 가능
    def get(self, request):
        user = request.user
        serialized_user_data = UserSignupSerializer(user).data
        return Response(serialized_user_data, status=status.HTTP_200_OK)


    # def get(self, request):
    #     return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    #회원가입
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입 완료!"})
        else:
            print(serializer.errors)
            return Response({"message": "가입 실패!"})


    #@로그아웃
    def delete(self, request):
        logout(request)
        return Response({"message": "logout success!"})
