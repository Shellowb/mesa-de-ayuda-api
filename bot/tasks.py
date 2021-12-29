from __future__ import absolute_import, unicode_literals
import datetime
from celery import shared_task
from django.core.checks import messages
from django.db.models.lookups import In
import django.utils.timezone as tz
from instances.models import Instance, Steps
from instances.serializers import InstanceSerializer, StepsSerializer
from botUsers.models import BotUser, Notification, Subscription, SubscriptionLink, BotUserPermissions

# Send Messages
TELEGRAM_URL = "https://api.telegram.org/bot"
from API.settings import BOT_TOKEN
import json
import requests

@shared_task
def send_notification_test():
    tg_id = 187579960
    inst = Instance.objects.get(name="Proceso de Titulación primavera 2021")
    next_events = Steps.objects.filter(instance=inst)
    steps_setializer = StepsSerializer(next_events, many=True)
    notification = {"msg": "", "chat_id": tg_id}
    link = 'mesadeayuda.cadcc.cl'
    for step in steps_setializer.data:
        notification["msg"] += markup_clearner(f"{step['name']} {step['end_date']}\n") #\\n{step['description']}\\n
    notification["msg"] += f"para revisar más fechas visita [mesa de ayuda]({link})"
    return notification

def get_notification_test():
    tg_id = 187579960
    inst = Instance.objects.get(name="Proceso de Titulación primavera 2021")
    next_events = Steps.objects.filter(instance=inst)
    steps_setializer = StepsSerializer(next_events, many=True)
    notification = {"msg": "", "chat_id": tg_id}
    link = 'mesadeayuda.cadcc.cl'
    for step in steps_setializer.data:
        notification["msg"] += markup_clearner(f"{step['name']} {step['end_date']}\n") #\\n{step['description']}\\n
    notification["msg"] += f"para revisar más fechas visita [mesa de ayuda]({link})"
    return notification

@shared_task
def suscribe_test(tg_id=187579960, target=None):
    ERR_USER = "Error al guardar el usuario"
    ERR_SUSBCRIPTION = "Error en el procesamiento de la suscripcion, intente más tarde"
    instance = Instance.objects.get(name='Proceso de Titulación primavera 2021')
    target = SubscriptionLink.Destiny.TO_STEPS
    chat = tg_id['chat_id']
    user = tg_id['id']

    if target is None:
       target = SubscriptionLink.Destiny.TO_STEPS

    try:
        link = SubscriptionLink.objects.get(instance=instance,destiny=target)
    except:
        link = SubscriptionLink()
        link.instance = instance
        link.destiny = target
        link.save() 
    try:
        new_user = BotUser.objects.get(uid=user)
        try:
            new_settings = BotUserPermissions.objects.get(user=new_user)
        except:
            new_settings = BotUserPermissions()
            new_settings.user = new_user
            new_settings.identity = True
            new_settings.subscriptions = True
            new_settings.save()
    except Exception as e:
        try:
            new_user = BotUser(uid=user)
            new_user.save()
            new_settings = BotUserPermissions()
            new_settings.user = new_user
            new_settings.identity = True
            new_settings.subscriptions = True
            new_settings.save()
        except Exception as e1:
            return ERR_USER
    try:
        print(new_user)
        try:
            new_subscription = new_subscription = Subscription.objects.get(bot_user=new_user, target_element=link)
        except:
            frequency = datetime.timedelta(minutes=3) #(days=20, hours=10)
            new_subscription = Subscription(bot_user=new_user, chat = chat, target_element=link, frequency=frequency)
            new_subscription.save()
            new_subscription = Subscription.objects.get(bot_user=new_user, target_element=link)

                #   Save Notification
            notification = Notification()
            notification.subscription = new_subscription
            notification.msg = get_notification_test()
            notification.next_notification = tz.now() + new_subscription.frequency
            notification.save()
        message = markup_clearner(f'Nueva suscripción {new_subscription}')
    except Exception as e:
        print(e)
        message = ERR_SUSBCRIPTION
    
    return message


def async_send(message, chat_id, keyboard_button={}):
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

@shared_task
def send_today_notifications():
    notifications = Notification.get_today_notifications()
    messages = [] #[{"text": '', "keyboard": {}}]
    print(len(notifications))
    for notification in notifications:
        print(notification.msg)
        msg = markup_clearner(f'{notification.msg}')
        try:
            notf_susc = notification.subscription
            notf_chat = notf_susc.chat
            print(notf_chat)
        except:
            notf_chat = None
        notf_message = {'text': msg, 'keyboard': {}, 'chat': notf_chat}
        messages.append(notf_message)

    for msg in messages:
        if msg['chat'] is None:
            continue
        async_send(msg['text'], msg['chat'], msg['keyboard'])



@shared_task
def subscribe(tg_id, target):
    ERR_USER = "Error al guardar el usuario"
    ERR_PERMISSIONS = "Su usuario no tiene los permisos de subscripción habilitados"
    ERR_SUSBCRIPTION = "Error en el procesamiento de la subscripción, intente más tarde"
    tg_chat = tg_id['chat_id']
    tg_user = tg_id['id']
    new_user = BotUser.get_create_bot_user(tg_user)
    print(new_user)
    try:
        new_subscription = Subscription(bot_user=new_user, chat=tg_chat, instance=None)
    except Exception as e:
        print(e)
        message = f'ERR_SUSBCRIPTION'
    return message

    #  bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    # chat = models.IntegerField()
    # target_element = models.ForeignKey(SubscriptionLink, on_delete=models.CASCADE)
    # frequency = models.DurationField()
    # created_at = models.DateTimeField(auto_now_add=True)
    
    

def markup_clearner(text: str):
    especial_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for ch in especial_characters:
        text = text.replace( ch , '\\' + ch)
    return text

