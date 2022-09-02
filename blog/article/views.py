from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import ArticleSerializer


# Create your views here.

class ArticleAPIList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
