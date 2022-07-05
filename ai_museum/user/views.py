from django.contrib.auth import login, authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.views.decorators.csrf import csrf_exempt
from user.serializers import UserSignupSerializer, UserSerializer


# 사용자에게 토큰을 할당하기 위한 구성
from user.jwt_claim_serializer import SpartaTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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


    # 회원탈퇴
    def delete(self, request):
        return Response({"message": "delete method!!"})

    # 로그아웃
    # def logout(request):
        # return Response({"message": "logout success!"})


# 토큰 할당
class SpartaTokenObtainPairView(TokenObtainPairView):
    serializer_class = SpartaTokenObtainPairSerializer