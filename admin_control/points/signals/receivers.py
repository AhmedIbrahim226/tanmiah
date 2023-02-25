from django.db.models.signals import pre_save, post_save
from ..models import Point, PointFunction, TotalPoint
from users.models import UserAuth


# Dispatch immediately point functions added
def dispatch_add_point(sender, instance, using, **kwargs):
    TotalPoint.objects.bulk_create([
        TotalPoint(point=instance, user=user) for user in UserAuth.objects.all()
    ], ignore_conflicts=True)


post_save.connect(receiver=dispatch_add_point, sender=Point)