from channels.layers import get_channel_layer


async def forum_broadcast_message(subscriber):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"forum_user_{str(subscriber.id)}",
        {
            'type': 'new_message',
        }
    )