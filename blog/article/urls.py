from django.urls import path

from .views import *

urlpatterns = [
    path('articles/', ArticleAPIList.as_view())
]