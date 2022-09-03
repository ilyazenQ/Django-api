from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=255, unique=True, db_index=True, verbose_name='Заголовок')
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True, blank=True)
    time_update = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey(User, related_name='posts', verbose_name='Пользователь', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_update']
