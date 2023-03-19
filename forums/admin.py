from django.contrib import admin
from .models import Forum, ForumFile, Discussion, DiscussionComment, Answer, AnswerComment


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    readonly_fields = ('last_updated',)


@admin.register(ForumFile)
class ForumFileAdmin(admin.ModelAdmin):
    """"""


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    readonly_fields = ('ret_created_at', 'ret_at_date_time')
    filter_horizontal = ('vote',)
    list_display = ['title', 'tag_list', 'view', 'votes', 'verified', 'safe']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    
    def votes(self, obj):
        return obj.vote.all().count()

@admin.register(DiscussionComment)
class DiscussionCommentAdmin(admin.ModelAdmin):
    """"""
    readonly_fields = ('at', )

    def at(self, obj):
        return obj.ret_naturaltime_created

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """"""
    filter_horizontal = ('vote',)


@admin.register(AnswerComment)
class AnswerCommentAdmin(admin.ModelAdmin):
    """"""