from django.db import models

from forums.models import Discussion, DiscussionComment, Answer, AnswerComment
from posts.models import Post


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


class ReviewingSystem(models.Model):
    on_add_discussion = models.BooleanField(default=False)
    on_add_discussion_comment = models.BooleanField(default=False)
    on_add_answer = models.BooleanField(default=False)
    on_add_answer_comment = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'reviewing system'
        verbose_name_plural = 'reviewing systems'
