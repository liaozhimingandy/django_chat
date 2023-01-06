import uuid

from django.contrib import auth
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.apps import apps
from django.utils.translation import gettext_lazy as _

from user.lib import LeafSnowFlake

# 生成雪花序号
leaf_snowflake = LeafSnowFlake.IdWorker(data_center_id=settings.DATA_CENTER_ID, worker_id=settings.DATA_CENTER_ID)


class WLUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, password=password,**extra_fields)
        # user.password = make_password(password) # 保存用户信息时已加密,此处无需加密
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(
            self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

    @staticmethod
    def _uid_default():
        return f"wlid_{str(leaf_snowflake.get_id(useragent='left-snowflake-uid'))}"

    sex_code = (
        (0, '未知'),
        (1, '男'),
        (2, '女')
    )
    user_type_choices = (
        (0, '系统用户'),
        (1, '普通用户'),
    )
    id = models.AutoField(primary_key=True)
    uid = models.CharField("用户id", null=False, unique=True, blank=False, help_text='用户id',
                           max_length=32, default='wlid_'+str(uuid.uuid4()).replace('-', '')[:12])
    nick_name = models.CharField('用户昵称', null=True, blank=False, help_text='用户昵称', max_length=64)
    username = models.CharField(unique=True, null=True, blank=False, help_text='登录名', max_length=64, verbose_name="登录名")
    email = models.CharField(null=True, blank=True, help_text='电子邮箱', max_length=64, verbose_name='电子邮箱')
    mobile = models.CharField(null=True, blank=True, help_text='手机号码', max_length=16, verbose_name='手机号码')
    sex = models.SmallIntegerField(null=False, choices=sex_code, help_text='性别', default=0,  verbose_name='性别')
    avatar = models.CharField(null=True, max_length=128, help_text='头像图片', verbose_name='头像图片')
    user_status = models.CharField(null=True, default=True, help_text='用户状态信息,用户自定义', max_length=64,
                                   verbose_name='用户状态信息,用户自定义')
    user_type = models.SmallIntegerField(null=False, choices=user_type_choices, help_text='用户类型', default=1,
                                         verbose_name='用户类型')
    login_ip = models.GenericIPAddressField(help_text='最后登录ip', default='127.0.0.1', verbose_name='最后登录ip')
    last_login = models.DateTimeField(null=False, help_text='最后登录时间', auto_now_add=True, verbose_name='最后登录时间')
    gmt_created = models.DateTimeField(null=False, help_text='创建时间', auto_now_add=True, verbose_name='创建时间')
    is_staff = models.BooleanField(_("staff status"),
                                   default=False,
                                   help_text=_("Designates whether the user can log into this admin site.")
                                   )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ), )
    is_superuser = models.BooleanField(
            _("superuser status"),
            default=False,
            help_text=_(
                "Designates that this user has all permissions without "
                "explicitly assigning them."
            ),
        )
    # 处理AttributeError: type object 'User' has no attribute 'USERNAME_FIELD'
    USERNAME_FIELD = 'username'

    objects = WLUserManager()

    class Meta(AbstractBaseUser.Meta):
        db_table = 'wl_user'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name
    
    def save(self, *args, **kwargs):
        self.password = make_password(password=self.password, salt=None, hasher='pbkdf2_sha256')
        super(User, self).save(*args, **kwargs)