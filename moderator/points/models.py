from datetime import timedelta

from django.db import models
from django.utils.functional import cached_property

from posts.models import Post
from users.models import UserAuth


class Point(models.Model):
    singular_name = models.CharField(max_length=50, unique=True)
    plural_name = models.CharField(max_length=50, unique=True)
    img = models.ImageField(upload_to='point/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.singular_name


class PointFunction(models.Model):
    WHEN_CHOICES = (
        (1, 'Add post without media'),
        (2, 'Add post with media'),
        (3, 'Comment on specific post'),
    )

    TIMES_LIMITED = (
        (1, 'Unlimited'),
        (2, 'Per minute'),
        (3, 'Per hour'),
        (4, 'Per day'),
        (5, 'Per week'),
        (6, 'Per month'),
        (7, 'Per year'),
    )

    point = models.ForeignKey(to=Point, on_delete=models.CASCADE, related_name='point_functions')
    when = models.SmallIntegerField(choices=WHEN_CHOICES)
    comment_on_post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=True, blank=True)
    times = models.PositiveSmallIntegerField()
    times_limited = models.SmallIntegerField(choices=TIMES_LIMITED, default=1)
    earn = models.PositiveSmallIntegerField()
    maximum_to_earn = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    deduction = models.BooleanField(default=False)

    class Meta:
        unique_together = ('point', 'when')

    def __str__(self):
        return self.get_when_str

    @cached_property
    def get_times_limited_str(self):
        if self.times_limited == 1:
            return 'Unlimited'
        elif self.times_limited == 2:
            return 'Per minute'
        elif self.times_limited == 3:
            return 'Per hour'
        elif self.times_limited == 4:
            return 'Per day'
        elif self.times_limited == 5:
            return 'Per week'
        elif self.times_limited == 6:
            return 'Per month'
        elif self.times_limited == 7:
            return 'Per year'

    @cached_property
    def get_when_str(self):
        if self.when == 1:
            return 'Add post without media'
        elif self.when == 2:
            return 'Add post with media'
        elif self.when == 3:
            return 'Comment on specific post'

    @cached_property
    def get_times_limited_timedelta(self):
        if self.times_limited == 1:
            return None
        elif self.times_limited == 2:
            return timedelta(minutes=1)
        elif self.times_limited == 3:
            return timedelta(hours=1)
        elif self.times_limited == 4:
            return timedelta(days=1)
        elif self.times_limited == 5:
            return timedelta(weeks=1)
        elif self.times_limited == 6:
            return timedelta(weeks=4.34524)
        elif self.times_limited == 7:
            return timedelta(weeks=12 * 4.34524)

    @cached_property
    def key_prefix(self):
        if self.when == 1:
            return '{}_add_post_without_media{}'.format(self.point.singular_name.replace(' ', '_').lower(),
                                                        '_deduction' if self.deduction else '')
        elif self.when == 2:
            return '{}_add_post_with_media{}'.format(self.point.singular_name.replace(' ', '_').lower(),
                                                     '_deduction' if self.deduction else '')
        elif self.when == 3:
            return '{}_comment_on_specific_post{}'.format(self.point.singular_name.replace(' ', '_').lower(),
                                                          '_deduction' if self.deduction else '')


class UserPointFunctionEarning(models.Model):
    owner = models.ForeignKey(UserAuth, on_delete=models.CASCADE, related_name='user_point_function_earn')
    point_function = models.ForeignKey(PointFunction, on_delete=models.CASCADE, related_name='point_function_earn')
    earns_until_now = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "{} : {}".format(self.point_function.get_when_str, self.owner.username)

    class Meta:
        unique_together = ('owner', 'point_function')

    @cached_property
    def get_max_to_earn(self):
        return self.point_function.maximum_to_earn


class TotalPoint(models.Model):
    point = models.ForeignKey(to=Point, on_delete=models.CASCADE, related_name='total_point_functions')
    user = models.ForeignKey(to=UserAuth, on_delete=models.CASCADE, related_name='user_total_point_functions')
    total_earning = models.SmallIntegerField(default=0)

    def __str__(self):
        return "{} : {}".format(self.user.username, self.point.singular_name)

    class Meta:
        unique_together = ('point', 'user')


class PointLog(models.Model):
    point = models.ForeignKey(to=Point, on_delete=models.CASCADE, related_name='point_logs')
    log = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
