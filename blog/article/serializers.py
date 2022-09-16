from rest_framework import serializers

from .models import *


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('pk', 'title', 'content', 'user', 'time_create', 'time_update')


class ArticleDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = ('pk', 'title', 'content', 'user', 'time_create', 'time_update')


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'username', 'posts')


class UserSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSub
        fields = ('user', 'sub')

class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRead
        fields = ('user', 'article')
