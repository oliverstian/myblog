# from rest_framework import generics
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
#
# from .models import Article
# from .serializers import ArticleSerializer
#
#
# @api_view()  # 用来把view转换成apiview
# def article_list(request):
#     articles = Article.objects.filter(status=Article.STATUS_NORMAL)
#     article_serializers = ArticleSerializer(articles, many=True)
#     return Response(article_serializers.data)
#
#
# class ArticleList(generics.ListCreateAPIView):
#     queryset = Article.objects.filter(status=Article.STATUS_NORMAL)
#     serializer_class = ArticleSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.filter(status=Article.STATUS_NORMAL)
    # permission_classes = [IsAdminUser]











































