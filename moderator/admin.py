from asgiref.sync import async_to_sync
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.db.models import F

from notices.models import ForumNotice
from posts.models import PostMedia
from users.models import UserAuth
from utils.websocket_messages import forum_broadcast_message
from .models import PostProxy, DiscussionProxy, DiscussionCommentProxy, AnswerProxy, AnswerCommentProxy, ReviewingSystem
from .points.models import PointFunction, UserPointFunctionEarning, TotalPoint, PointLog


class PostMediaInline(admin.TabularInline):
    model = PostMedia

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def manage_point_functions_on_post(obj, functions):
    if functions.exists():
        for func in functions:
            check_to_increase, created = UserPointFunctionEarning.objects.get_or_create(
                owner=obj.owner,
                point_function=func,
                defaults={'earns_until_now': func.earn}
            )
            if func.deduction:
                if not check_to_increase.earns_until_now + func.earn > check_to_increase.get_max_to_earn:
                    TotalPoint.objects.filter(point=func.point, user=obj.owner).update(
                        total_earning=F('total_earning') - func.earn)
                    log_message = f'{func.earn} points are deducted from the user {obj.owner.username} from point: {func.point.singular_name} ==> {func.get_when_str}'
                    PointLog.objects.create(point=func.point, log=log_message)
                    if not created:
                        check_to_increase.earns_until_now += func.earn
                        check_to_increase.save()
            else:
                if not check_to_increase.earns_until_now + func.earn > check_to_increase.get_max_to_earn:
                    TotalPoint.objects.filter(point=func.point, user=obj.owner).update(
                        total_earning=F('total_earning') + func.earn)
                    log_message = f'{func.earn} points earned by the user {obj.owner.username} from point: {func.point.singular_name} ==> {func.get_when_str}'
                    PointLog.objects.create(point=func.point, log=log_message)
                    if not created:
                        check_to_increase.earns_until_now += func.earn
                        check_to_increase.save()


@admin.register(PostProxy)
class PostProxyAdmin(admin.ModelAdmin):
    filter_horizontal = ('share_with',)

    def has_add_permission(self, request):
        return False

    def get_inlines(self, request, obj):
        if obj.media != 4:
            return [PostMediaInline]
        return super().get_inlines(request, obj)

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.model._meta.fields if field.name != 'safe'] +
            [field.name for field in self.model._meta.many_to_many]
        ))

    def save_model(self, request, obj, form, change):
        if change and not obj.safe:
            return super().save_model(request, obj, form, change)

        if obj.point_game:
            """without media option media = 4"""
            if obj.media == 4:
                functions = PointFunction.objects.select_related('point').filter(when=1, active=True)
                manage_point_functions_on_post(obj, functions)
                return super().save_model(request, obj, form, change)
            else:
                """with media option media = [1 | 2 | 3]"""
                functions = PointFunction.objects.select_related('point').filter(when=2, active=True)
                manage_point_functions_on_post(obj, functions)
                return super().save_model(request, obj, form, change)
        return super().save_model(request, obj, form, change)


# Forums config
@admin.register(DiscussionProxy)
class DiscussionProxyAdmin(admin.ModelAdmin):
    filter_horizontal = ('vote',)
    list_display = ['title', 'tag_list', 'view', 'votes', 'verified', 'safe']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())

    def votes(self, obj):
        return obj.vote.all().count()

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.model._meta.fields if
             field.name not in ('safe', 'verified', 'created_at', 'at_date_time')] + ['ret_created_at',
                                                                                      'ret_at_date_time'] +
            [field.name for field in self.model._meta.many_to_many]
        ))

    def save_model(self, request, obj, form, change):
        if change and not obj.safe:
            return super().save_model(request, obj, form, change)

        forum_subscribers = obj.forum.subscribers.all()
        for subscriber in forum_subscribers:
            if obj.author != subscriber:
                ForumNotice.objects.create(sender_discussion=obj.forum, recipient=subscriber,
                                           content=f'new discussion add to forum {obj.forum.name}')
                # call websocket signal here for notify
                async_to_sync(forum_broadcast_message)(subscriber)

        forum = obj.forum
        forum.last_updated = obj.at_date_time
        forum.save()
        return super().save_model(request, obj, form, change)


@admin.register(DiscussionCommentProxy)
class DiscussionCommentProxyAdmin(admin.ModelAdmin):
    def _created_at(self, obj):
        return obj.ret_created

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.model._meta.fields if
             field.name not in ('safe', 'created_at', 'at_date_time')] + ['_created_at', 'ret_at_date_time'] +
            [field.name for field in self.model._meta.many_to_many]
        ))

    def save_model(self, request, obj, form, change):
        if change and not obj.safe:
            return super().save_model(request, obj, form, change)

        forum_subscribers = obj.discussion.forum.subscribers.all()
        author = obj.author
        for subscriber in forum_subscribers:
            if author != subscriber:
                ForumNotice.objects.create(sender_discussion_comment=obj, recipient=subscriber,
                                           content=f'new comment on discussion {obj.discussion.title} in forum {obj.discussion.forum}')
                # call websocket signal here for notify
                async_to_sync(forum_broadcast_message)(subscriber)

        discussion_subscribers = obj.discussion.subscribers.all()
        for subscriber in discussion_subscribers:
            if author != subscriber:
                ForumNotice.objects.create(sender_discussion_comment=obj, recipient=subscriber,
                                           content=f'new comment on discussion {obj.discussion.title} in forum {obj.discussion.forum}')
                # call websocket signal here for notify
                async_to_sync(forum_broadcast_message)(subscriber)
        return super().save_model(request, obj, form, change)


@admin.register(AnswerProxy)
class AnswerProxyAdmin(admin.ModelAdmin):
    filter_horizontal = ('vote',)
    list_display = ['__str__', 'votes', 'verified', 'safe']

    def votes(self, obj):
        return obj.vote.all().count()

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.model._meta.fields if
             field.name not in ('safe', 'verified', 'created_at', 'at_date_time')] + ['ret_created_at',
                                                                                      'ret_at_date_time'] +
            [field.name for field in self.model._meta.many_to_many]
        ))

    def save_model(self, request, obj, form, change):
        if change and not obj.safe:
            return super().save_model(request, obj, form, change)

        forum_subscribers = obj.discussion.forum.subscribers.all()
        author = obj.author
        for subscriber in forum_subscribers:
            if author != subscriber:
                ForumNotice.objects.create(sender_answer=obj, recipient=subscriber,
                                           content=f'new answer on discussion {obj.discussion.title} in forum {obj.discussion.forum}')
                # call websocket signal here for notify
                async_to_sync(forum_broadcast_message)(subscriber)

        discussion_subscribers = obj.discussion.subscribers.all()
        for subscriber in discussion_subscribers:
            if author != subscriber:
                ForumNotice.objects.create(sender_answer=obj, recipient=subscriber,
                                           content=f'new answer on discussion {obj.discussion.title} in forum {obj.discussion.forum}')
                # call websocket signal here for notify
                async_to_sync(forum_broadcast_message)(subscriber)

        discussion = obj.discussion
        discussion.time_case = 2
        discussion.at_date_time = obj.at_date_time
        discussion.save()
        return super().save_model(request, obj, form, change)


@admin.register(AnswerCommentProxy)
class AnswerCommentProxyAdmin(admin.ModelAdmin):
    def _created_at(self, obj):
        return obj.ret_created

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.model._meta.fields if
             field.name not in ('safe', 'created_at', 'at_date_time')] + ['_created_at', 'ret_at_date_time'] +
            [field.name for field in self.model._meta.many_to_many]
        ))

    def save_model(self, request, obj, form, change):
        if change and not obj.safe:
            return super().save_model(request, obj, form, change)

        forum_subscribers = obj.answer.discussion.forum.subscribers.all()
        author = obj.author
        for subscriber in forum_subscribers:
            if author != subscriber:
                ForumNotice.objects.create(sender_answer_comment=obj, recipient=subscriber,
                                           content=f'new answer comment on discussion {obj.answer.discussion.title} in forum {obj.answer.discussion.forum}')
                # call websocket signal here for notify
                async_to_sync(forum_broadcast_message)(subscriber)

        discussion_subscribers = obj.answer.discussion.subscribers.all()
        for subscriber in discussion_subscribers:
            if author != subscriber:
                ForumNotice.objects.create(sender_answer_comment=obj, recipient=subscriber,
                                           content=f'new answer comment on discussion {obj.answer.discussion.title} in forum {obj.answer.discussion.forum}')
                # call websocket signal here for notify
                async_to_sync(forum_broadcast_message)(subscriber)
        return super().save_model(request, obj, form, change)


@admin.register(ReviewingSystem)
class ReviewingSystemAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        data = form.cleaned_data
        for action in data:
            if data[action]:
                if action == 'on_add_discussion':
                    perm = Permission.objects.get(codename='denied_to_add_safe_discussion',
                                                  content_type__app_label='forums')
                    for user in UserAuth.objects.filter(is_user=True):
                        user.user_permissions.add(perm)
                elif action == 'on_add_discussion_comment':
                    perm = Permission.objects.get(codename='denied_to_add_safe_discussion_comment',
                                                  content_type__app_label='forums')
                    for user in UserAuth.objects.filter(is_user=True):
                        user.user_permissions.add(perm)
                elif action == 'on_add_answer':
                    perm = Permission.objects.get(codename='denied_to_add_safe_answer',
                                                  content_type__app_label='forums')
                    for user in UserAuth.objects.filter(is_user=True):
                        user.user_permissions.add(perm)
                elif action == 'on_add_answer_comment':
                    perm = Permission.objects.get(codename='denied_to_add_safe_answer_comment',
                                                  content_type__app_label='forums')
                    for user in UserAuth.objects.filter(is_user=True):
                        user.user_permissions.add(perm)
            else:
                if action == 'on_add_discussion':
                    perm = Permission.objects.get(codename='denied_to_add_safe_discussion',
                                                  content_type__app_label='forums')
                    for user in UserAuth.objects.filter(is_user=True):
                        user.user_permissions.remove(perm)
                elif action == 'on_add_discussion_comment':
                    perm = Permission.objects.get(codename='denied_to_add_safe_discussion_comment',
                                                  content_type__app_label='forums')
                    for user in UserAuth.objects.filter(is_user=True):
                        user.user_permissions.remove(perm)
                elif action == 'on_add_answer':
                    perm = Permission.objects.get(codename='denied_to_add_safe_answer',
                                                  content_type__app_label='forums')
                    for user in UserAuth.objects.filter(is_user=True):
                        user.user_permissions.remove(perm)
                elif action == 'on_add_answer_comment':
                    perm = Permission.objects.get(codename='denied_to_add_safe_answer_comment',
                                                  content_type__app_label='forums')
                    for user in UserAuth.objects.filter(is_user=True):
                        user.user_permissions.remove(perm)

        return super().save_model(request, obj, form, change)
