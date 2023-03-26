import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from notices.api.serializers import ForumNoticeSerializer
from notices.models import ForumNotice
from ..models import Forum, Discussion


class ForumFollowingNotification(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None
        self.user = None

    async def connect(self):
        self.user = self.scope.get('user')
        self.group_name = f"forum_user_{str(self.user.id)}"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        print('disconnect called')
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        msg_type = content.get('type')
        if msg_type == 'new_forum_subscribe':
            forum_id = content.get('forum_id')
            await self.add_new_subscribe_to_forum(forum_id)

        elif msg_type == 'new_discussion_subscribe':
            discussion_id = content.get('discussion_id')
            await self.add_new_subscribe_to_discussion(discussion_id)

    async def new_message(self, event):
        notices = await self.get_user_notices()
        await self.send_json({'notices': notices})

    @database_sync_to_async
    def get_user_notices(self):
        notices = ForumNotice.objects.filter(recipient=self.user, is_read=False)
        _serial = ForumNoticeSerializer(notices, many=True)
        serial_ = json.dumps(_serial.data)
        serial = json.loads(serial_)
        return serial

    @database_sync_to_async
    def add_new_subscribe_to_forum(self, forum_id):
        forum = Forum.objects.get(id=forum_id)
        for discussion in forum.forum_discussions.all():
            discussion.subscribers.remove(self.user)
        forum.subscribers.add(self.user)

    @database_sync_to_async
    def add_new_subscribe_to_discussion(self, discussion_id):
        discussion = Discussion.objects.get(id=discussion_id)
        if self.user not in discussion.forum.subscribers.all():
            discussion.subscribers.add(self.user)
