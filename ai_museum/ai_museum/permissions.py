from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission
from rest_framework import status
from datetime import timedelta ,datetime
from django.utils import timezone

class RegisteredMoreThanThreeDaysUser(BasePermission):
    
    message = '가입 후 3일 이상 지난 사용자만 사용할 수 있습니다.'

    def has_permission(self, request, view):
        user = request.user

        return bool(user.is_authenticated and request.user.join_date < (timezone.now() - timedelta(days=3)))


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code = status_code
        super().__init__(detail=detail, code=code)


class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    # admin 사용자는 모두 가능 // 로그인 사용자는 조회만
    SAFE_METHODS = ('GET',)
    message = '접급 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response = {
                    "detail": "서비스를 이용하기 위해서 로그인을 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)


        # admin 사용자이거나 가입일이 7일 이상 된 사용자의 경우 True 
        if user.is_authenticated and user.is_admin or \
            user.join_date < (datetime.now().date() - timedelta(days=7)):
            return True

        # 로그인 사용자가 get 요청 시 True
        if user.is_authenticated and request.method in self.SAFE_METHODS:
            return True

        return False