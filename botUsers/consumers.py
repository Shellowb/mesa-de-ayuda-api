import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from bot import views
from bot.models import Chat, Messages
from bot.serializers import ChatSerializer, MessagesSerializer

# class BotUserConsumer(AsyncWebsocketConsumer):
#     pass