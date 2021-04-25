import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from bot import views
from bot.models import Chat, Messages
from bot.serializers import ChatSerializer, MessagesSerializer

class ChatConsumer(AsyncWebsocketConsumer):

  @sync_to_async  
  def get_messages(self):
    return Messages().last_messages(self.room_name, 20)

  @sync_to_async
  def save_message(self, message, chat_id, bot=False):
    chat = None
    try: 
      chat_instance = Chat.objects.get(chat_id=chat_id)
      chat_serializer = ChatSerializer(chat_instance)
      chat = chat_serializer.data
    except Chat.DoesNotExist:
      print('No existe esta conversacion de telegram')

    message_data = {
      'chat_id': int(chat_id),
      'text': message,
      'fromTelegram': bot,
    }
    message_serializer = MessagesSerializer(data=message_data)
    if message_serializer.is_valid():
      message_serializer.save()

  async def fetch_messages(self):
    for message in await self.get_messages():
      await self.send(text_data=json.dumps({
        'message': message.text,
        'fromTelegram': message.fromTelegram,
      }))

  async def new_message(self, message, bot=False):
    # Send message to room group
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'chat_message',
        'message': message
      }
    )
    await self.save_message(message, self.room_name, bot)

  async def send_to_bot(self, chat_id, message):
    views.BotView.send_message(message ,chat_id)

  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = 'chat_%s' % self.room_name

    # Join room group
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )

    await self.accept()

  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )

  # Receive message from WebSocket
  async def receive(self, text_data):
    text_data_json = json.loads(text_data)

    if text_data_json['command'] == 'fetch_messages':
      await self.fetch_messages()
    elif text_data_json['command'] == 'new_message':
      await self.new_message(text_data_json['message'], text_data_json['bot'])

      if not text_data_json['bot']:
        await self.send_to_bot(self.room_name, text_data_json['message'])
        

  # Receive message from room group
  async def chat_message(self, event):
    message = event['message']

    # Send message to WebSocket
    await self.send(text_data=json.dumps({
      'message': message
    }))