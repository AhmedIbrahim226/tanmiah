from django.db import models
from django.utils.functional import cached_property
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime

from users.models import UserAuth




class Point(models.Model):
    singular_name = models.CharField(max_length=50)
    plural_name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='point/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.singular_name


class PointFunction(models.Model):
    WHEN_CHOICES = (
        (1, 'Add post without media'),
        (2, 'Add post with media'),
        (3, 'Add post specific post'),
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
    times = models.PositiveSmallIntegerField()
    times_limited = models.SmallIntegerField(choices=TIMES_LIMITED, default=1)
    earn = models.PositiveSmallIntegerField()
    maximum_to_earn = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    deduction = models.BooleanField(default=False)


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
            return 'Add post specific post'


class TotalPointFunction(models.Model):
    point = models.ForeignKey(to=Point, on_delete=models.CASCADE, related_name='total_point_functions')
    user = models.ForeignKey(to=UserAuth, on_delete=models.CASCADE, related_name='total_point_function')
    total_earning = models.PositiveSmallIntegerField()
