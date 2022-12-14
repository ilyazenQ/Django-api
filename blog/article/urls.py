from django.urls import path

from .views import *

urlpatterns = [
    path('articles/', ArticleAPIList.as_view()),
    path('articles-filters/', ArticleWithFiltersAPIList.as_view()),
    path('article/create/', ArticleAPICreate.as_view()),
    path('sub/', UserSubAPI.as_view()),
    path('read/', UserReadAPI.as_view()),
    path('sublist/', ArticleSubAPIList.as_view()),
    path('users/', UserAPIList.as_view()),
    path('article/<int:pk>/', ArticleAPIDetailView.as_view()),
]