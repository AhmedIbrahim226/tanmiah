from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .dispatch import signal_1
from ..models import Post, PostMedia
import os


def delete_postmedia_files(sender, instance, using, **kwargs):
    if instance.img:
        os.remove(instance.img.path) if os.path.exists(instance.img.path) else ""
    elif instance.video:
        os.remove(instance.video.path) if os.path.exists(instance.video.path) else ""
    elif instance.document:
        os.remove(instance.document.path) if os.path.exists(instance.document.path) else ""


pre_delete.connect(receiver=delete_postmedia_files, sender=PostMedia)
