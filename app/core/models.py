"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    # AbstractUser:カスタマイズの柔軟性は低いがコーディング量は少ない
    # AbstractBaseUser:カスタマイズの柔軟性は高いがコーディング量は多い
    AbstractBaseUser,
    # BaseUserManager:ユーザーを生成する時使うヘルパー(Helper)クラス
    BaseUserManager,
    # AbstractBaseUserはパーミッション関連の機能を持っていないので、
    # パーミッションの機能を利用したい場合は、PermissionsMixinを同時に継承しておく
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """
    Manager for users.
    ヘルパー(Helper)クラスであるBaseUserManagerは3つのファンクションを持っている
    _create_user,create_user,create_superuser
    """

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        # normalize_email:Normalize the email address by lowercasing the domain part of it.
        # 電子メール アドレスのドメイン部分を小文字にして正規化します。
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # using:Managerが使用するDBを指定する
        # _dbはdefault
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    # Login with Django admin
    is_staff = models.BooleanField(default=False)

    # ヘルパークラスを使うように設定
    objects = UserManager()

    # ユーザーモデル検索のためのキーとなるフィールドを指定
    USERNAME_FIELD = "email"


class Recipe(models.Model):
    """Recipe objects."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title
