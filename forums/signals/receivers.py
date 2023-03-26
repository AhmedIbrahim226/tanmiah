from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from notices.models import ForumNotice
from utils.websocket_messages import forum_broadcast_message
from ..models import Discussion, DiscussionComment, Answer, AnswerComment


def dispatch_add_discussion(sender, instance, using, **kwargs):
    if kwargs.get('created'):
        author = instance.author
        if instance.safe:
            forum_subscribers = instance.forum.subscribers.all()
            for subscriber in forum_subscribers:
                if author != subscriber:
                    notice = ForumNotice.objects.create(sender_discussion=instance, recipient=subscriber,
                                               content=f'new discussion add to forum {instance.forum.name}')
                    # call websocket signal here for notify
                    async_to_sync(forum_broadcast_message)(subscriber)

        if author not in instance.forum.subscribers.all():
            instance.subscribers.add(author)


post_save.connect(receiver=dispatch_add_discussion, sender=Discussion)


def dispatch_add_discussion_comment(sender, instance, using, **kwargs):
    if kwargs.get('created'):
        if instance.safe:
            forum_subscribers = instance.discussion.forum.subscribers.all()
            author = instance.author
            for subscriber in forum_subscribers:
                if author != subscriber:
                    ForumNotice.objects.create(sender_discussion_comment=instance, recipient=subscriber,
                                               content=f'new comment on discussion {instance.discussion.title} in forum {instance.discussion.forum}')
                    # call websocket signal here for notify
                    async_to_sync(forum_broadcast_message)(subscriber)

            discussion_subscribers = instance.discussion.subscribers.all()
            for subscriber in discussion_subscribers:
                if author != subscriber:
                    ForumNotice.objects.create(sender_discussion_comment=instance, recipient=subscriber,
                                               content=f'new comment on discussion {instance.discussion.title} in forum {instance.discussion.forum}')
                    # call websocket signal here for notify
                    async_to_sync(forum_broadcast_message)(subscriber)


post_save.connect(receiver=dispatch_add_discussion_comment, sender=DiscussionComment)


def dispatch_add_answer(sender, instance, using, **kwargs):
    if kwargs.get('created'):
        if instance.safe:
            forum_subscribers = instance.discussion.forum.subscribers.all()
            author = instance.author
            for subscriber in forum_subscribers:
                if author != subscriber:
                    ForumNotice.objects.create(sender_answer=instance, recipient=subscriber,
                                               content=f'new answer on discussion {instance.discussion.title} in forum {instance.discussion.forum}')
                    # call websocket signal here for notify
                    async_to_sync(forum_broadcast_message)(subscriber)

            discussion_subscribers = instance.discussion.subscribers.all()
            for subscriber in discussion_subscribers:
                if author != subscriber:
                    ForumNotice.objects.create(sender_answer=instance, recipient=subscriber,
                                               content=f'new answer on discussion {instance.discussion.title} in forum {instance.discussion.forum}')
                    # call websocket signal here for notify
                    async_to_sync(forum_broadcast_message)(subscriber)


post_save.connect(receiver=dispatch_add_answer, sender=Answer)


def dispatch_add_answer_comment(sender, instance, using, **kwargs):
    if kwargs.get('created'):
        if instance.safe:
            forum_subscribers = instance.answer.discussion.forum.subscribers.all()
            author = instance.author
            for subscriber in forum_subscribers:
                if author != subscriber:
                    ForumNotice.objects.create(sender_answer_comment=instance, recipient=subscriber,
                                               content=f'new answer comment on discussion {instance.answer.discussion.title} in forum {instance.answer.discussion.forum}')
                    # call websocket signal here for notify
                    async_to_sync(forum_broadcast_message)(subscriber)

            discussion_subscribers = instance.answer.discussion.subscribers.all()
            for subscriber in discussion_subscribers:
                if author != subscriber:
                    ForumNotice.objects.create(sender_answer_comment=instance, recipient=subscriber,
                                               content=f'new answer comment on discussion {instance.answer.discussion.title} in forum {instance.answer.discussion.forum}')
                    # call websocket signal here for notify
                    async_to_sync(forum_broadcast_message)(subscriber)


post_save.connect(receiver=dispatch_add_answer_comment, sender=AnswerComment)
