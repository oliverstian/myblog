"""
Django settings for myblog project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(BASE_DIR)  # 改为basedir为项目目录（即外层myblog）


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0z-3ab$+*k69e_nl&-pzewjj*cc)eq!whx)vxoj5eed34gz5yv'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "blog",
    "comment",
    "config",
    "user",
    "rest_framework",
    "xadmin",
    "crispy_forms",
    # "DjangoUeditor",
    "ckeditor",
    "ckeditor_uploader",  # 上传图片用
    "imagekit",
]

MIDDLEWARE = [
    "blog.middleware.user_id.UserIDMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myblog.urls'

THEME = "bootstrap"
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "myblog", "themes", THEME, "templates")],
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

WSGI_APPLICATION = 'myblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# django认证系统使用的模型类。加上这个设置，用户管理相关信息就会保存在自己创建的User表中
# 而不是Django内置的表中
AUTH_USER_MODEL = 'user.User'
LOGIN_URL = "/user/login"

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


THEME = 'bootstrap'
STATIC_ROOT = '/tmp/static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "myblog", "themes", THEME, "static")
]

MEDIA_URL = "/media/"  # 对比STATIC_URL和STATIC_ROOT
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # 绝对路径，里面存放文件

DEFAULT_FILE_STORAGE = 'myblog.storage.WatermarkStorage'  # 文件存储引擎

# ckeditor配置项
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 工具条功能
        'height': 300,  # 编辑器高度
        'width': 800,  # 编辑器宽度
        'tabSpaces': 4,
        'extraPlugins': 'codesnippet',
    },
}
CKEDITOR_UPLOAD_PATH = "article_images"  # MEDIA_ROOT下的这个文件夹下
CKEDITOR_BROWSE_SHOW_DIRS = True  # 好像没什么卵用,加个吧

# 配置缓存使用redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:181855@makesi@134.175.30.49:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}











