from django.views import View
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from channels.http import AsgiRequest

from bot.telegram.parsing import Parser
from bot.models import Chat, Messages
from bot.serializers import ChatSerializer, MessagesSerializer

parser = Parser()


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def chat_list(request):
  """
    GET list of chat
  """
  if request.method == 'GET':
    chats = Chat.objects.all()
    
    chats_serializer = ChatSerializer(chats, many=True)
    return JsonResponse(chats_serializer.data, safe=False)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def first_message(request, id_chat):
  """
    GET first message
  """
  if request.method == 'GET':
    message = Messages().last_messages(id_chat, 1)
    message_serializer = MessagesSerializer(message, many=True)
    return JsonResponse(message_serializer.data, safe=False)


class BotView(View):
  def post(self, request: AsgiRequest, *args, **kwargs):
    update = request.body
    parser.decode_update(update)
    return JsonResponse({"ok": "POST request processed"})

  def get(self, request: AsgiRequest, *args, **kwargs):
    update = request.body
    print("GET", update.decode())