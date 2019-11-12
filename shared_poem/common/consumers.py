from channels.generic.websocket import AsyncWebsocketConsumer
import json


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
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
