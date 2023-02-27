"""
Configure points functions with db signals
"""

from django.db.models.signals import post_save
from posts.models import Post
from django.db.models import F
from ..models import Point, PointFunction, UserPointFunctionEarning, TotalPoint
from ..ratelimit import RateLimit


def manage_ratelimit_and_earns(func, user=None):
    user_rate_limit = RateLimit(
        key=f"_{user.id}",
        limit=func.times,
        period=func.get_times_limited_timedelta,
        key_prefix=func.key_prefix
    ).check()
    if user_rate_limit:
        check_to_increase, created = UserPointFunctionEarning.objects.get_or_create(
            owner=user,
            point_function=func,
            defaults={'earns_until_now': func.earn}
        )
        if func.deduction:
            if not check_to_increase.earns_until_now + func.earn > check_to_increase.get_max_to_earn:
                TotalPoint.objects.filter(point=func.point, user=user).update(
                    total_earning=F('total_earning') - func.earn)
                if not created:
                    check_to_increase.earns_until_now += func.earn
                    check_to_increase.save()
            return

        if not check_to_increase.earns_until_now + func.earn > check_to_increase.get_max_to_earn:
            TotalPoint.objects.filter(point=func.point, user=user).update(
                total_earning=F('total_earning') + func.earn)
            if not created:
                check_to_increase.earns_until_now += func.earn
                check_to_increase.save()
        return

# Add post without media
def add_post_without_media(sender, instance, using, **kwargs):
    """without media option media = 4"""

    if kwargs.get('created'):
        if instance.media == 4:
            functions = PointFunction.objects.select_related('point').filter(when=1, active=True)
            if functions.exists():
                for func in functions:
                    manage_ratelimit_and_earns(func, instance.owner)

# Add post with media
def add_post_with_media(sender, instance, using, **kwargs):
    """with media option media = [1 | 2 | 3]"""

    if kwargs.get('created'):
        if instance.media != 4:
            functions = PointFunction.objects.select_related('point').filter(when=2, active=True)
            if functions.exists():
                for func in functions:
                    manage_ratelimit_and_earns(func, instance.owner)




post_save.connect(receiver=add_post_without_media, sender=Post)
post_save.connect(receiver=add_post_with_media, sender=Post)
