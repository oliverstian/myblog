"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from blog.views import (
    IndexView, CategoryView, TagView,
    ArticleDetailView, SearchView, AuthorView,
)
from config.views import (
    LinkListView,
)
from comment.views import (
    add_comment_view,
)
from user.views import (
    RegisterView, LoginView, LogoutView,
    UserInfoView,
)
# from blog.apis import article_list, ArticleList
from rest_framework.routers import DefaultRouter
from blog.apis import ArticleViewSet

router = DefaultRouter()
router.register(r"article", ArticleViewSet, base_name="api-article")

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r"^$", IndexView.as_view(), name="index"),
    re_path(r"^category/(?P<category_id>\d+)/$", CategoryView.as_view(), name="category-list"),
    re_path(r"^tag/(?P<tag_id>\d+)/$", TagView.as_view(), name="tag-list"),

    re_path(r"^article/(?P<article_id>\d+)\.html/$", ArticleDetailView.as_view(), name="article-detail"),
    re_path(r"^search/$", SearchView.as_view(), name="search"),
    re_path(r"^author/(?P<owner_id>\d+)/$", AuthorView.as_view(), name="author"),
    re_path(r"^links/$", LinkListView.as_view(), name="links"),
    re_path(r"comment/$", add_comment_view, name="add_comment"),

    re_path(r"register/$", RegisterView.as_view(), name="register"),
    re_path(r"login/$", LoginView.as_view(), name="login"),
    re_path(r"logout/$", LogoutView.as_view(), name="logout"),
    re_path(r"userinfo/$", UserInfoView.as_view(), name="userinfo"),


    # re_path(r"^api/article/", article_list, name="article-list"),
    # re_path(r"^api/article/", ArticleList.as_view(), name="article-list")
    # re_path(r"^api/", include(router.urls, namespace="api")),
]


















