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
    instance = Instance.objects.get(name='Proceso de Titulación primavera 2021')
    if target is None:
        target = Steps.objects.get(instance=instance).first()
    
    new_user = BotUser.objects.get(uid=tg_id)
    if not new_user:
        new_user = BotUser(uid=tg_id)
        new_user.save()

    new_subscription = Subscription(bot_user=new_user, instance=instance, target=target)
    new_subscription.save()


def markup_clearner(text: str):
    especial_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for ch in especial_characters:
        text = text.replace( ch , '\\' + ch)
    return text