from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# custom user model


class User(AbstractBaseUser):
    # unique=True 설정으로 중복값을 방지
    username = models.CharField("사용자 계정", max_length=30, unique=True)
    # 패스워드는 암호화되어 저장되기 때문에 max_length를 넉넉하게 설정
    password = models.CharField("사용자 비밀번호", max_length=200)

    email = models.EmailField("사용자 이메일", max_length=254)
    join_date = models.DateTimeField("가입일", auto_now_add=True)

    is_private = models.BooleanField(default=True)

    # is_staff 에서 해당 값 사용
    is_admin = models.BooleanField(default=False)

    # username 을 아이디로 사용하겠다.
    USERNAME_FIELD = 'username'

    ''' user를 생성할 때 입력받은 필드 지정
    사용할 일이 거의 없음 '''
    REQUIRED_FIELDS = []

    # custom user 생성 시 필요
    objects = UserManager()

    def __str__(self):
        return f"{self.username}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # admin 권한 설정
    @property
    def is_staff(self):
        return self.is_admin
