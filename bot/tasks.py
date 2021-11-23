from __future__ import absolute_import, unicode_literals
from celery import shared_task
from instances.models import Instance, Steps
from instances.serializers import InstanceSerializer, StepsSerializer


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
    for step in steps_setializer.data:
        notification["msg"] += f"**{step['name']}** {step['end_date']}\n{step['description']}\n"
    notification["msg"] += f"para revisar más fechas visita http://localhost:3000/categorias/1/instancia/1"
    return notification