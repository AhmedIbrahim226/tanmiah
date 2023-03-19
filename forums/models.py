from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.utils.functional import cached_property

from users.models import UserAuth
from taggit.managers import TaggableManager


class ForumFile(models.Model):
    file = models.FileField(upload_to='forums/')


class Forum(models.Model):
    name = models.CharField(max_length=50, unique=True)
    bg = models.ImageField(upload_to='forums/bg/')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @cached_property
    def ret_naturaltime_updated(self):
        return naturaltime(self.last_updated)


class Discussion(models.Model):
    author = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name='author_forum_discussions')
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='forum_discussions')

    title = models.CharField(max_length=400)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    time_case = models.PositiveSmallIntegerField(choices=[(1, 'asked'), (2, 'answered')], default=1)
    at_date_time = models.DateTimeField(auto_now=True)

    verified = models.BooleanField(default=False)
    vote = models.ManyToManyField(to=UserAuth, blank=True)
    view = models.PositiveSmallIntegerField(default=0)
    tags = TaggableManager()

    # admin permission
    safe = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     forum = self.forum
    #     forum.last_updated = self.created_at
    #     forum.save()
    #     return super().save(args, kwargs)

    def __str__(self):
        return self.title
    
    @cached_property
    def ret_time_case(self):
        if self.time_case == 1:
            return 'asked'
        elif self.time_case == 2:
            return 'answered'
    
    @cached_property
    def ret_at_date_time(self):
        return naturaltime(self.at_date_time)
    
    @cached_property
    def ret_created_at(self):
        return naturaltime(self.created_at)

    
    @cached_property
    def get_answers_count(self):
        return self.answers.count()
    
    @cached_property
    def get_answers(self):
        return self.answers.all()
    
    @cached_property
    def get_comments(self):
        return self.discussion_comments.all()

class DiscussionComment(models.Model):
    author = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name='user_discussion_comments')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='discussion_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # admin permission
    safe = models.BooleanField(default=False)

    @cached_property
    def ret_created(self):
        return naturaltime(self.created_at)


class Answer(models.Model):
    author = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name='user_discussion_answers')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    verified = models.BooleanField(default=False)
    vote = models.ManyToManyField(to=UserAuth, blank=True)

    # admin permission
    safe = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     discussion = self.discussion
    #     discussion.time_case = 2
    #     discussion.at_date_time = self.created_at
    #     discussion.save()
    #     return super().save(args, kwargs)
    
    @cached_property
    def ret_created_at(self):
        return naturaltime(self.created_at)
    
    
    @cached_property
    def get_comments(self):
        return self.answer_comments.all()


class AnswerComment(models.Model):
    author = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name='user_answer_comments')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # admin permission
    safe = models.BooleanField(default=False)

    @cached_property
    def ret_created(self):
        return naturaltime(self.created_at)