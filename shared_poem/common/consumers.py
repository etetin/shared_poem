from channels.generic.websocket import AsyncWebsocketConsumer
from django_redis import get_redis_connection
import json


class Consumer(AsyncWebsocketConsumer):
    _redis = get_redis_connection("default")
    _user_agent = None

    async def connect(self):
        for l in self.scope['headers']:
            if l[0].decode('utf-8') == 'user-agent':
                self._user_agent = l[1].decode("utf-8")
                break

        # Join group
        await self.channel_layer.group_add(
            'main_page',
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            'main_page',
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        symbol = text_data_json['symbol']

        if len(symbol) == 1:
            if not self._redis.exists(f'useragent:{self._user_agent}') and self._user_agent is not None:
                self._redis.set(f'useragent:{self._user_agent}', 'temp', ex=300)
                self._redis.append('poem', symbol)

                await self.channel_layer.group_send(
                    'main_page',
                    {
                        'type': 'poem_symbols',
                        'symbol': symbol
                    }
                )

    async def poem_symbols(self, event):
        symbol = event['symbol']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'symbol': symbol
        }))
