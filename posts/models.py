from django.db import models
from users.models import UserAuth
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.core.files.images import get_image_dimensions


class Album(models.Model):
    PRIVACY = ((1, _('Public')), (2, _('All members')), (3, _('just me')),)

    name = models.CharField(max_length=50)
    owner = models.ForeignKey(to=UserAuth, on_delete=models.CASCADE, related_name='albums')
    privacy = models.SmallIntegerField(choices=PRIVACY, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'owner')

    @cached_property
    def get_privacy_str(self):
        """"""
        if self.privacy == 1:
            return _('Public')
        elif self.privacy == 2:
            return _('All members')
        elif self.privacy == 3:
            return _('just me')

    @cached_property
    def ret_naturalday_created(self):
        return naturalday(self.created_at)

    @cached_property
    def get_photos_number(self):
        length = self.album_media.values_list('img', flat=True).exclude(img__exact='', img__isnull=False)
        return len(length)

    @cached_property
    def get_videos_number(self):
        length = self.album_media.values_list('video', flat=True).exclude(video__exact='', video__isnull=False)
        return len(length)


class Folder(models.Model):
    PRIVACY = ((1, _('Public')), (2, _('All members')), (3, _('just me')),)

    name = models.CharField(max_length=50)
    parent_folder = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='sub_folder')
    owner = models.ForeignKey(to=UserAuth, on_delete=models.CASCADE, related_name='folders')
    privacy = models.SmallIntegerField(choices=PRIVACY, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'owner')

    @cached_property
    def get_privacy_str(self):
        """"""
        if self.privacy == 1:
            return _('Public')
        elif self.privacy == 2:
            return _('All members')
        elif self.privacy == 3:
            return _('Just me')

    @cached_property
    def ret_naturalday_created(self):
        return naturalday(self.created_at)


class Post(models.Model):
    PRIVACY = ((1, _('Public')), (2, _('All members')), (3, _('just me')))
    MEDIA_INCLUDE = ((1, _('img')), (2, _('video')), (3, _('document')), (4, _('no thing')))

    owner = models.ForeignKey(to=UserAuth, on_delete=models.CASCADE, related_name='posts')
    privacy = models.SmallIntegerField(choices=PRIVACY, default=1)
    media = models.SmallIntegerField(choices=MEDIA_INCLUDE, default=4)
    description = models.TextField(help_text=_("Share with us what's on your mind.."), null=True, blank=True)
    share_with = models.ManyToManyField(UserAuth, related_name='posts_with_me', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


    @cached_property
    def get_privacy_str(self):
        """"""
        if self.privacy == 1:
            return _('Public')
        elif self.privacy == 2:
            return _('All members')
        elif self.privacy == 3:
            return _('just me')

    @cached_property
    def ret_naturaltime_created(self):
        return naturaltime(self.created_at)


class PostMedia(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=True, blank=True, related_name='post_media')
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE, null=True, blank=True, related_name='album_media')
    folder = models.ForeignKey(to=Folder, on_delete=models.CASCADE, null=True, blank=True, related_name='folder_docs')
    img = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True)
    document = models.FileField(upload_to='posts/docs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @cached_property
    def ret_naturaltime_created(self):
        return naturaltime(self.created_at)

    @cached_property
    def ret_naturalday_created(self):
        return naturalday(self.created_at)


class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
