from rest_framework import serializers
from bot.models import Messages, Chat


class MessagesSerializer(serializers.ModelSerializer):

  class Meta:
    model = Messages
    fields = (
      'id',
      'chat_id',
      'text',
      'fromTelegram',
      'created_at'
    )

class ChatSerializer(serializers.ModelSerializer):

  class Meta:
    model = Chat
    fields = (
      'id',
      'chat_id',
      'first_name',
      'last_name',
      'username'
    )