"""
Django settings for django_welink project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import logging
import os
import subprocess
import time
from datetime import timedelta
from pathlib import Path

from django import get_version

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "APP_SECRET_KEY", "django-insecure-&(s=fs#s3b9&=8&y_+bhzquk_1-uq)iu@=v=%+&qegp9958%e$"
)

# 应用版本号
# VERSION = (1, 0, 2, "alpha", 3)
# __version__ = get_version(VERSION)
__version__ = os.getenv('APP_VERSION', '1.0')
APP_COMMIT_HASH = os.getenv('APP_COMMIT_HASH', '')
if not APP_COMMIT_HASH:
    APP_COMMIT_HASH = subprocess.check_output(["git", "rev-parse", '--short', "HEAD"]).decode('UTF8').strip()
APP_BRANCH = os.getenv('APP_BRANCH', '')
if not APP_BRANCH:
    APP_BRANCH = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode('UTF8').strip()
APP_ENV = 'Production' if int(os.environ.get("DEBUG", default=0)) else 'Develop'
APP_VERSION_VERBOSE = f"{__version__}({APP_ENV}•{APP_BRANCH}•{APP_COMMIT_HASH})"
print(f"version information: {APP_VERSION_VERBOSE}")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("APP_DEBUG", default=1))
ALLOWED_HOSTS = os.getenv("APP_DJANGO_ALLOWED_HOSTS", "*").split(" ")
CSRF_TRUSTED_ORIGINS = os.getenv("APP_CSRF_TRUSTED_ORIGINS", "http://*").split(" ")


# Application definition
# 官方app
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",  # 站点使用
    "django.contrib.admindocs"
]
# 第三方app
THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',  # 添加：跨域组件
    'django_filters',
]

# 本地app
LOCAL_APPS = [
    "moment",
    # Your stuff: custom apps go here
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_welink.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_welink.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# 静态文件
STATIC_URL = os.getenv("APP_STATIC_URL", 'static/')
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# 多媒体文件
MEDIA_URL = os.getenv("APP_MEDIA_URL", 'media/')
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
# python manage.py collectstatic 收集文件到下面文件文件夹里
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 默认为False，设置True许跨域时携带Cookie
# 用于处理跨域问题
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'https://alsoapp.gnway.cc',
    'http://alsoapp.gnway.cc',
    'http://welink.alsoapp.com',
    'https://welink.alsoapp.com',
    # 这里需要注意： 1. 必须添加http://否则报错（https未测试） 2. 此地址就是允许跨域的地址，即前端地址
)

# drestf 设置
REST_FRAMEWORK = {
    # 分页设置
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # 指定过滤后端
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend', ],

    'DEFAULT_THROTTLE_CLASSES': (  # 定义限流类
        'rest_framework.throttling.AnonRateThrottle',  # 匿名用户限流
        'rest_framework.throttling.UserRateThrottle',  # 登录用户限流
        'rest_framework.throttling.ScopedRateThrottle'  # 针对某一个接口限流（只能在APIView类使用）
    ),
    # 定义限流速率（支持天数/时/分/秒的限制）;`second`, `minute`, `hour` 或`day`来指明周期
    'DEFAULT_THROTTLE_RATES': {
        'anon': '128/day',
        'user': '1024/day',
    },

    # 异常处理
    # 'EXCEPTION_HANDLER': 'luffy.utils.exceptions.custom_exception_handler',

    # 定义认证配置
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',  # jwt认证
        'rest_framework.authentication.BasicAuthentication',  # 基本认证
        'rest_framework.authentication.SessionAuthentication',  # session认证
        # 'user.lib.TokenUtil.JWTAuthentication',  # token全局认证
    ),
    # 默认权限设置
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    )
}

# 站点
SITE_ID = os.getenv('APP_SITE_ID', 2024)

##########################################################################################
# MinIO服务器地址及认证信息
MINIO_ACCESS_KEY = os.getenv('APP_MINIO_ACCESS_KEY', 'chat')
MINIO_SECRET_KEY = os.getenv('APP_MINIO_SECRET_KEY', 'chat1234')
MINIO_SCHEMA = os.getenv('APP_MINIO_SCHEMA', 'http://')
MINIO_ENDPOINT = os.getenv('APP_MINIO_ENDPOINT', '172.16.33.188:10005')  # MinIO服务器地址
MINIO_BUCKET = os.getenv('APP_MINIO_BUCKET', 'chatapp')

# 设置文件默认存储
DEFAULT_FILE_STORAGE = 'moment.MyStorage.MinioStorage'
##########################################################################################