"""
Configure points functions with db signals
"""

from django.db.models.signals import post_save
from posts.models import Post

# Add post without media
def add_post_without_media(sender, instance, using, **kwargs):
    """without media option media = 4"""

    if kwargs.get('created'):
        if instance.media == 4:
            """"""


post_save.connect(receiver=add_post_without_media, sender=Post)
