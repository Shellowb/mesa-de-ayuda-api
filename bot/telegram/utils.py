# Default Python
import json
from markdownify import markdownify

#Django
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.mail import send_mail
from rest_framework import status
import requests

# Configuration
from API.settings import EMAIL_HOST_USER, BOT_TOKEN, TELEGRAM_URL
# Bot
from bot.wspython import *

# Models & Serializers
from django.contrib.auth.models import User
from process.models import Process
from bot.models import Chat
from category.models import Category
from faq.models import FAQs
from process.serializers import ProcessSerializer
from category.serializers import CategorySerializer
from faq.serializers import FAQSerializer
from bot.serializers import ChatSerializer

# Telegram made library
from bot.telegram.objects.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

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


def get_process_keyboard(dumped=False) -> InlineKeyboardMarkup or str:
    processes = Process.objects.filter(published=True).order_by('-created_at')
    processes_serializer = ProcessSerializer(processes, many=True)
    buttons = [
        InlineKeyboardButton(
                text=process['name'],
                callback_data = f'id:{process["id"]}, "label": "Process"'
            )
     for process in processes_serializer.data]

    if dumped:
        return json.dumps(InlineKeyboardMarkup(inline_keyboard=[buttons]), separators=(',', ':'))

    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def get_name_process(id):
    processes = Process.objects.get(pk=id)
    processes_serializer = ProcessSerializer(processes)
    return processes_serializer.data['name']


def dislike_question(id_faq):
    try: 
        faq = FAQs.objects.get(pk=id_faq)
    except FAQs.DoesNotExist:
        return JsonResponse({'message': 'The question does not exist'}, status=status.HTTP_404_NOT_FOUND)

    faq_serializer = FAQSerializer(faq, data={'dislikes': FAQSerializer(faq).data['dislikes'] + 1}) 
    if faq_serializer.is_valid(): 
        faq_serializer.save() 


def like_question(id_faq):
    try: 
        faq = FAQs.objects.get(pk=id_faq)
    except FAQs.DoesNotExist:
        return JsonResponse({'message': 'The question does not exist'}, status=status.HTTP_404_NOT_FOUND)

    faq_serializer = FAQSerializer(faq, data={'likes': FAQSerializer(faq).data['likes'] + 1}) 
    if faq_serializer.is_valid(): 
        faq_serializer.save() 


def get_category_keyboard(id_process):
    categories = Category.objects.filter(process=id_process).order_by('-created_at')
    categories_serializer = CategorySerializer(categories, many=True)
    keyboard = [[{"text": category['name'], "callback_data": json.dumps({"id": str(category['id']), "label": "Category"}) }] for category in categories_serializer.data]
    return {"inline_keyboard": keyboard}


def get_name_category(id):
    categories = Category.objects.get(pk=id)
    categories_serializer = CategorySerializer(categories)
    return categories_serializer.data['name']


def get_questions_keyboard(id_category):
    faqs = FAQs.objects.filter(category=id_category).filter(published=True).order_by('-created_at')
    faqs_serializer = FAQSerializer(faqs, many=True)
    keyboard = [[{"text": faq['question'], "callback_data": json.dumps({"id": str(faq['id']), "label": "Question"}) }] for faq in faqs_serializer.data]
    return {"inline_keyboard": keyboard}


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
