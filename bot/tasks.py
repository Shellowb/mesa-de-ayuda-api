from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.db.models.lookups import In
from instances.models import Instance, Steps
from instances.serializers import InstanceSerializer, StepsSerializer
from botUsers.models import BotUser, Subscription

@shared_task
def add(x, y):
    return x + y

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

@shared_task
def suscribe_test(tg_id=187579960, target=None):
    ERR_USER = "Error al guardar el usuario"
    ERR_SUSBCRIPTION = "Error en el procesamiento de la suscripcion, intente más tarde"
    instance = Instance.objects.get(name='Proceso de Titulación primavera 2021')
    chat = tg_id['chat_id']
    user = tg_id['id']

    if target is None:
        target = Steps.objects.filter(instance=instance).first()
    
    try:
        new_user = BotUser.objects.get(uid=user)
    except Exception as e:
        try:
            new_user = BotUser(uid=user)
            new_user.save()
        except Exception as e1:
            return ERR_USER
    try:
        print(new_user)
        new_subscription = Subscription(bot_user=new_user, chat = chat ,instance=instance, target_element=target)
        new_subscription.save()
        new_subscription = Subscription.objects.get(uid=user)
        message = f'Nueva suscripción {new_subscription}'
    except Exception as e:
        print(e)
        message = f'ERR_SUSBCRIPTION'
    return message

def markup_clearner(text: str):
    especial_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for ch in especial_characters:
        text = text.replace( ch , '\\' + ch)
    return text