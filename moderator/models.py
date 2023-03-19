from django.db import models

from posts.models import Post
from forums.models import Discussion, DiscussionComment, Answer, AnswerComment

class PostProxy(Post):
    class Meta:
        proxy = True
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class DiscussionProxy(Discussion):
    class Meta:
        proxy = True
        verbose_name = 'discussion'
        verbose_name_plural = 'discussions'


class DiscussionCommentProxy(DiscussionComment):
    class Meta:
        proxy = True
        verbose_name = 'discussion comment'
        verbose_name_plural = 'discussion comments'


class AnswerProxy(Answer):
    class Meta:
        proxy = True
        verbose_name = 'answer'
        verbose_name_plural = 'answers'

class AnswerCommentProxy(AnswerComment):
    class Meta:
        proxy = True
        verbose_name = 'answer comment'
        verbose_name_plural = 'answer comments'
