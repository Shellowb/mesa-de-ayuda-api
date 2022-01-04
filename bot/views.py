from django.shortcuts import render
from channels.generic.websocket import WebsocketConsumer
from markdownify import markdownify
from bot.wspython import *
import json
import websockets
import asyncio
import os

# Models & Serializers
from process.models import Process
from instances.models import Instance
from bot.models import Chat, Messages
from botUsers.models import SubscriptionLink, BotUserPermissions
from category.models import Category
from faq.models import FAQs
from process.serializers import ProcessSerializer
from category.serializers import CategorySerializer
from faq.serializers import FAQSerializer
from bot.serializers import ChatSerializer, MessagesSerializer

from django.core.mail import send_mail
from API.settings import EMAIL_HOST_USER, BOT_TOKEN

import requests
from django.views import View
from bot import consumers


from django.http.response import JsonResponse
from django.utils.safestring import mark_safe
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import User


from bot.tasks import subscribe, suscribe_test, markup_clearner, send_today_notifications
from bot.test_tasks import add

TELEGRAM_URL = "https://api.telegram.org/bot"

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

def send_mail_notification(message, chat):
  first_name = chat['first_name']
  last_name = chat['last_name']
  emails = User.objects.filter(is_active=True).exclude(email='').values_list('email', flat=True)
  send_mail(
    'Nuevo mensaje en Mesa de Ayuda DCC',
    f'Hay un nuevo mensaje en el chat de Mesa de Ayuda DCC\nDe: {first_name} {last_name}\nMensaje: {message}',
    EMAIL_HOST_USER,
    emails,
    fail_silently=False
  )

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
  def post(self, request, *args, **kwargs):
    t_data = json.loads(request.body)
    print("-----", t_data)
    label = None
    question=None
    try:
      t_message = t_data['message']
      t_chat = t_message['chat']
      t_chat['chat_id'] = t_chat['id']
      text = t_message["text"].strip()
    except Exception as e:
      try:
        t_chat = t_data['callback_query']['message']['chat']
        t_chat['chat_id'] = t_chat['id']
        data = json.loads(t_data['callback_query']['data'])

        text = data['id']
        label = data['label']
        if label=='Feedback':
          question = data['question']
      except Exception as e:
        return JsonResponse({"ok": "POST request processed"})

    self.message_processing(t_chat, text, label, question)

    return JsonResponse({"ok": "POST request processed"})

  def message_processing(self, t_chat, message, label=None, question=None ):
    messages = []
    if label is None:
      if message == '/start':
        messages = [
          {"text": 'Hola, soy Turing y estoy aqui para ayudarte con tus dudas frecuentes', "keyboard": {}},
          {"text": 'Recuerda que puedes obtener mas información sobre la mesa de ayuda DCC en [mesadeayuda\.cl](https://mesadeayuda.cadcc.cl)', "keyboard": {}},
          {"text": 'Actualmente puedo ayudarte con /preguntasFrecuentes de...', "keyboard": self.get_process_keyboard()},
          {"text": 'En caso de no poder contestar tu consulta, puedo contactar a un /asistente por este mismo canal', "keyboard": {}}
        ]
      elif message == '/preguntasFrecuentes':
        messages = [
          {"text": 'Actualmente puedo ayudarte con /preguntasFrecuentes de...', "keyboard": self.get_process_keyboard()}
        ]
      elif message == '/asistente':
        messages = [
          {"text": 'Okey, te contactare con un@ asistente. Por favor ingresa tu consulta acontinuación', "keyboard": {}}
        ]
      # Test Command
      elif message == '/notificacion':
        send_today_notifications()
        send_today_notifications.delay()
        add.delay(4,4)
        messages = [
            {"text": 'notf', "keyboard": {}}
          ]

      elif message == '/subscription_options':
        msg = ""
        for choice in SubscriptionLink.Destiny.choices:
          msg += f'{choice[0]} {choice[1]}\n'
        # for instance in Instance.objects.all
        messages = [
            {"text": msg, "keyboard": {}}
          ]
      elif message == '/subscription_test':
          msg = suscribe_test(tg_id=t_chat)
          messages = [
            {"text": msg, "keyboard": {}}
          ]
      elif message == 'subscription':
        msg = subscribe(t_chat,t_chat,1)

      elif message == '/settings':
        msg = BotUserPermissions.set_permissions(user_id=t_chat,id=True, sub=True, sup=True)
        print(msg)
        msg = markup_clearner(msg)
        messages = [
          {"text": msg, "keyboard": {}}
        ]
      else:
        self.send_message_website(message, t_chat)
        messages = [
          {"text": 'He enviado el mensaje a nuestrxs asistentes, en breve te responderemos por este canal', "keyboard": {}}
        ]
    elif label == 'Process':
      name = self.get_name_process(int(message))
      messages = [
          {"text": 'Sobre que área de {} quieres saber?'.format(name), "keyboard": self.get_category_keyboard(int(message))}
      ]
    elif label == 'Category':
      name = self.get_name_category(int(message))
      messages = [
          {"text": 'Estas son las preguntas mas frecuentes de {}'.format(name), "keyboard": self.get_questions_keyboard(int(message))}
      ]
    elif label == 'Question':
      messages = self.get_question(int(message))
    elif label == 'Feedback':
      if message == 'Yes':
        self.like_question(int(question))
        messages = [
            {"text": 'Me alegra haberte ayudado... Si tienes mas consultas no dudes en preguntarme, revisar mis /preguntasFrecuentes o contactar a un /asistente', "keyboard": {}},
        ]
      if message == 'No':
        self.dislike_question(int(question))
        keyboard = {"inline_keyboard" : [
          [{"text": "Si", "callback_data": json.dumps({"id": "/asistente", "label": None}) }, {"text": "No", "callback_data": json.dumps({"id": "No", "label": "Helper"}) }],
        ]}
        messages = [
            {"text": 'Oh no, ¿Quieres que te contacte con un@ asistente para que resuelva tu consulta?', "keyboard": keyboard},
        ]
    elif label == 'Helper':
      if message == 'No':
        messages = [
            {"text": 'Bueno, cualquier consulta puede revisar mis otras /preguntasFrecuentes o contactar a un /asistente', "keyboard": {}},
        ]

    for msg in messages:
      self.send_message(msg['text'], t_chat["id"], msg['keyboard'])


  @staticmethod
  def get_process_keyboard():
    processes = Process.objects.filter(published=True).order_by('-created_at')
    processes_serializer = ProcessSerializer(processes, many=True)
    keyboard = [[{"text": process['name'], "callback_data": json.dumps({"id": str(process['id']), "label": "Process"}) }] for process in processes_serializer.data]
    return {"inline_keyboard": keyboard}

  @staticmethod
  def get_name_process(id):
    processes = Process.objects.get(pk=id)
    processes_serializer = ProcessSerializer(processes)
    return processes_serializer.data['name']

  @staticmethod
  def dislike_question(id_faq):
    try: 
      faq = FAQs.objects.get(pk=id_faq)
    except FAQs.DoesNotExist:
      return JsonResponse({'message': 'The question does not exist'}, status=status.HTTP_404_NOT_FOUND)

    faq_serializer = FAQSerializer(faq, data={'dislikes': FAQSerializer(faq).data['dislikes'] + 1}) 
    if faq_serializer.is_valid(): 
      faq_serializer.save() 
  
  @staticmethod
  def like_question(id_faq):
    try: 
      faq = FAQs.objects.get(pk=id_faq)
    except FAQs.DoesNotExist:
      return JsonResponse({'message': 'The question does not exist'}, status=status.HTTP_404_NOT_FOUND)

    faq_serializer = FAQSerializer(faq, data={'likes': FAQSerializer(faq).data['likes'] + 1}) 
    if faq_serializer.is_valid(): 
      faq_serializer.save() 

  @staticmethod
  def get_category_keyboard(id_process):
    categories = Category.objects.filter(process=id_process).order_by('-created_at')
    categories_serializer = CategorySerializer(categories, many=True)
    keyboard = [[{"text": category['name'], "callback_data": json.dumps({"id": str(category['id']), "label": "Category"}) }] for category in categories_serializer.data]
    return {"inline_keyboard": keyboard}

  @staticmethod
  def get_name_category(id):
    categories = Category.objects.get(pk=id)
    categories_serializer = CategorySerializer(categories)
    return categories_serializer.data['name']

  @staticmethod
  def get_questions_keyboard(id_category):
    faqs = FAQs.objects.filter(category=id_category).filter(published=True).order_by('-created_at')
    faqs_serializer = FAQSerializer(faqs, many=True)
    keyboard = [[{"text": faq['question'], "callback_data": json.dumps({"id": str(faq['id']), "label": "Question"}) }] for faq in faqs_serializer.data]
    return {"inline_keyboard": keyboard}

  @staticmethod
  def get_question(id_question):
    question = FAQs.objects.get(pk=id_question)
    faqs_serializer = FAQSerializer(question)

    keyboard = {"inline_keyboard" : [
      [{"text": "Si", "callback_data": json.dumps({"id": "Yes", "label": "Feedback", "question": str(faqs_serializer.data['id'])}) }, {"text": "No", "callback_data": json.dumps({"id": "No", "label": "Feedback", "question": str(faqs_serializer.data['id'])}) }],
    ]}
    return [
          {"text": '{}'.format(faqs_serializer.data['question']), "keyboard": {}},
          {"text": markdownify(faqs_serializer.data['answer'], heading_style="ATX"), "keyboard": {}},
          {"text": '¿Fue de útilidad la respuesta?', "keyboard": keyboard},
      ]

  @staticmethod
  def send_message_website(message, t_chat):
    chat = None
    try: 
      chat_instance = Chat.objects.get(chat_id=t_chat["id"])
      chat_serializer = ChatSerializer(chat_instance)
      chat = chat_serializer.data
    except Chat.DoesNotExist:
      chat_serializer = ChatSerializer(data=t_chat)
      if chat_serializer.is_valid():
        chat_serializer.save()
        chat = chat_serializer.data

    try:
      ws = Wspython()
      ws.send(t_chat["id"], message)
      send_mail_notification(message, chat)
    except Exception as e:
      print(e)
      print('I had some problems')

  @staticmethod
  def send_message(message, chat_id, keyboard_button={}):
    keyboard=json.dumps(keyboard_button)
    data = {
      "chat_id": chat_id,
      "text": message,
      "parse_mode": "MarkdownV2",
      'reply_markup': (None, keyboard)
    }
    response = requests.post(
      f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data
    )    
    res = response.json()
