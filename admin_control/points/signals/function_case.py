"""
Configure points functions with db signals
"""

from django.db.models.signals import post_save
from posts.models import Post
from django.db.models import F
from ..models import Point, PointFunction, UserPointFunctionEarning, TotalPoint
from ..ratelimit import RateLimit


def manage_ratelimit(func, user):
    user_rate_limit = RateLimit(
        key=f"_{user.id}",
        limit=func.times,
        period=func.get_times_limited_timedelta,
        key_prefix=func.key_prefix
    ).check()

    return user_rate_limit

# Add post point functions
def add_post_point_functions(sender, instance, using, **kwargs):
    if kwargs.get('created'):
        if instance.media == 4:
            """without media option media = 4"""
            functions = PointFunction.objects.select_related('point').filter(when=1, active=True)
            if functions.exists():
                for func in functions:
                    ratelimit = manage_ratelimit(func, instance.owner)
                    if ratelimit:
                        Post.objects.filter(id=instance.id).update(point_game=True)
            return
        else:
            """with media option media = [1 | 2 | 3]"""
            functions = PointFunction.objects.select_related('point').filter(when=2, active=True)
            if functions.exists():
                for func in functions:
                    ratelimit = manage_ratelimit(func, instance.owner)
                    if ratelimit:
                        Post.objects.filter(id=instance.id).update(point_game=True)
            return

post_save.connect(receiver=add_post_point_functions, sender=Post)
