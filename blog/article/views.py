from django.db.models import Count
from django.http import Http404
from django.shortcuts import render
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from .models import *
from .permissions import IsOwnerOrReadOnly
from .serializers import ArticleSerializer, UserSerializer, ArticleDetailSerializer


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

