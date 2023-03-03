from django.db import models

from posts.models import Post

class PostProxy(Post):
    class Meta:
        proxy = True
        verbose_name = 'post'
        verbose_name_plural = 'posts'
