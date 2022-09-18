from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, CoreAPIClient, force_authenticate, APIClient

from ..models import *


class ArticleTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        # create user
        self.user_response = self.client.post('http://127.0.0.1:8000/api/v1/auth/users/',
                                              {'username': 'testUser', 'password': 'testPassword'},
                                              format='json')

        self.user = User.objects.get(username='testUser')
        # get auth token
        self.token = self.client.post('http://127.0.0.1:8000/auth/token/login',
                                      {'username': 'testUser', 'password': 'testPassword'},
                                      format='json')
        # create user article
        self.article = Article.objects.create(title='testArticle',
                                              content='testContent',
                                              user=self.user)
        # create other user
        self.other_user = User.objects.create_user(username='otherUser', password='123')
        self.other_user_article = Article.objects.create(title='someName',
                                                         content='someContent',
                                                         user=self.other_user)
        # make auth
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.data['auth_token'])

    def test_create_user(self):
        user_created = User.objects.get(username='testUser')
        self.assertEqual(user_created.username, "testUser")
        self.assertEqual(self.user_response.status_code, 201)

    def test_get_user_token(self):
        get_token = self.client.post('http://127.0.0.1:8000/auth/token/login',
                                     {'username': 'testUser', 'password': 'testPassword'},
                                     format='json')
        self.assertEqual(get_token.data, self.token.data)

    def test_get_another_users_article(self):
        articles = self.client.get('http://127.0.0.1:8000/api/v1/articles/', format='json')
        self.assertEqual(articles.data[0]['title'], self.other_user_article.title)
        self.assertEqual(len(articles.data), 1)

    def test_create_article(self):
        article = self.client.post('http://127.0.0.1:8000/api/v1/article/create/',
                                   {'title': 'newArticle', 'content': 'newContent'}, format='json')
        self.assertEqual(Article.objects.get(title='newArticle').title, 'newArticle')
        self.assertEqual(len(Article.objects.filter(user=self.user)), 2)

    def test_get_users_list(self):
        users = self.client.get('http://127.0.0.1:8000/api/v1/users/', format='json')
        self.assertEqual(len(users.data), 2)

    def test_subscription_to_other_user(self):
        # should create
        created = self.client.post('http://127.0.0.1:8000/api/v1/sub/',
                                   {'sub': self.other_user.id}, format='json')
        self.assertEqual(created.data['status'], 'created')
        # should return Object already existing
        existing = self.client.post('http://127.0.0.1:8000/api/v1/sub/',
                                    {'sub': self.other_user.id}, format='json')
        self.assertEqual(existing.data['status'], 'Object already existing')
        # should return Object deleted
        deleted = self.client.delete('http://127.0.0.1:8000/api/v1/sub/',
                                     {'sub': self.other_user.id}, format='json')
        self.assertEqual(deleted.data['status'], 'Object deleted')

    def test_get_user_subscription_article_list(self):
        sub = self.client.post('http://127.0.0.1:8000/api/v1/sub/',
                               {'sub': self.other_user.id}, format='json')
        sub_articles = self.client.get('http://127.0.0.1:8000/api/v1/sublist/', format='json')
        self.assertEqual(dict(sub_articles.data)['count'], 1)
        self.assertEqual(dict(sub_articles.data)['results'][0]['title'], self.other_user_article.title)

    def test_make_article_read(self):
        new_article = Article.objects.create(title='testForRead', content='content', user=self.other_user)
        make_read = self.client.post('http://127.0.0.1:8000/api/v1/read/',
                                     {'article': new_article.id}, format='json')

        self.assertEqual(make_read.data['status'], 'Created')

    def test_get_article_read_list(self):
        new_article = Article.objects.create(title='testForRead', content='content', user=self.other_user)
        new_article2 = Article.objects.create(title='testForRead2', content='content', user=self.other_user)

        make_read = self.client.post('http://127.0.0.1:8000/api/v1/read/',
                                     {'article': new_article.id}, format='json')
        make_read2 = self.client.post('http://127.0.0.1:8000/api/v1/read/',
                                     {'article': new_article2.id}, format='json')
        # should return all articles
        articles_all = self.client.get('http://127.0.0.1:8000/api/v1/articles-filters/')
        self.assertEqual(len(articles_all.data), len(Article.objects.all()))
         # should return read article
        articles_read = self.client.get('http://127.0.0.1:8000/api/v1/articles-filters/?read=get')
        self.assertEqual(len(articles_read.data), 2)


