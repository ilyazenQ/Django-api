from django.db.models import Count
from django.http import Http404
from django.shortcuts import render
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import generics, status
from django.core import serializers
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import *
from .permissions import IsOwnerOrReadOnly
from .serializers import ArticleSerializer, UserSerializer, ArticleDetailSerializer, UserSubSerializer


# Create your views here.
# (4. Просматривать список постов других пользователей, отсортированный по дате
# создания, сначала свежие.)
class ArticleAPIList(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        articles = Article.objects.all()
        if self.request.user.is_authenticated:
            articles = Article.objects.exclude(user=self.request.user)
        if len(articles) == 0:
            raise Http404()
        return articles

class ArticleSubAPIPagination(PageNumberPagination):
    page_size = 10


#(6)
class ArticleSubAPIList(generics.ListAPIView):
    serializer_class = ArticleSerializer
    pagination_class = ArticleSubAPIPagination

    def get_queryset(self):
        subs = UserSub.objects.filter(user_id=self.request.user.id)
        sub_ids = []
        for sub in subs:
            sub_ids.append(sub.sub_id)
        articles = Article.objects.filter(user_id__in=sub_ids).order_by('-time_update')
        if len(articles) == 0:
            raise Http404()
        return articles

# (2. Авторизованным пользователям создавать посты. Пост имеет заголовок и текст
# поста. )
class ArticleAPICreate(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = (IsAuthenticated,)


# User RUD
class ArticleAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = (IsOwnerOrReadOnly,)


# (3. Просматривать список пользователей с возможностью сортировки по количеству
# постов.)
class UserAPIList(generics.ListAPIView):
    queryset = User.objects.annotate(post_count=Count("posts")).all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ('posts',)
    ordering = ('post_count',)

#5. Авторизованным пользователям подписываться и отписываться на посты других
#пользователей.
class UserSubAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        if not request.data['user_id'] or not request.data['sub_id']:
            return Response({"Expected more arguments"})
        try:
            user = User.objects.get(pk=request.data['user_id'])
            sub = User.objects.get(pk=request.data['sub_id'])
        except:
            return Response({"error": "Objects does not exists"})
        instance, created = UserSub.objects.get_or_create(
            user_id=request.data['user_id'],
            sub_id=request.data['sub_id'],
        )
        if created:
            return Response({"status": "created"})
        return Response({"status": "Object already existing"})

    def delete(self, request, *args, **kwargs):
        if not request.data['user_id'] or not request.data['sub_id']:
            return Response({"Expected more arguments"})
        try:
            user = User.objects.get(pk=request.data['user_id'])
            sub = User.objects.get(pk=request.data['sub_id'])
        except:
            return Response({"error": "Objects does not exists"})
        instance = UserSub.objects.get(
            user_id=request.data['user_id'],
            sub_id=request.data['sub_id'],
        ).delete()

        return Response({"status": "Object deleted"})