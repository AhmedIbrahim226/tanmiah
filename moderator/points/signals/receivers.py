from django.db.models.signals import pre_save, post_save, pre_delete
from ..models import Point, PointFunction, TotalPoint
from users.models import UserAuth
from django.core.cache import caches

# Dispatch immediately point functions added
def dispatch_add_point(sender, instance, using, **kwargs):
    TotalPoint.objects.bulk_create([
        TotalPoint(point=instance, user=user) for user in UserAuth.objects.all()
    ], ignore_conflicts=True)
post_save.connect(receiver=dispatch_add_point, sender=Point)


# Dispatch delete point function from cache
def dispatch_delete_point_function(sender, instance, using, **kwargs):
    cache = caches['ratelimiting']
    cache.delete_many([f"{instance.key_prefix}_{user.id}" for user in UserAuth.objects.all()])
pre_delete.connect(receiver=dispatch_delete_point_function, sender=PointFunction)
