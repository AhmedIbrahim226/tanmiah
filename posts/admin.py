from django.contrib import admin
from .models import Post, Album, PostMedia, Folder



@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """"""

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    # inlines = [InlinePostMedia]
    """"""

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('share_with', )

@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    """"""
