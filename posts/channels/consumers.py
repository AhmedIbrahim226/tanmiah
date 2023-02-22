from channels.generic.websocket import AsyncWebsocketConsumer
import json
from ..models import Post


class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('channel1', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print('Disconnected called')
        await self.channel_layer.group_discard('channel1', self.channel_name)


    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    # Msgs from out of self
    # async def manage_sending(self, event):
    #     establish_type = event.get('establish_type')
    #     context = event.get('context')
    #
    #     await self.send(json.dumps({'msg_type': establish_type, 'msg': context}))

