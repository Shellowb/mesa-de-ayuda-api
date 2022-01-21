import re
from celery import shared_task
from setuptools import Command
from instances.models import Instance

class SubscriptionCommand(Command):
    name = '/subscription'
    re = re.compile(r'\/subscription')

    @shared_task
    def suscribe_test(tg_id=187579960, target=None):
        ERR_USER = "Error al guardar el usuario"
        ERR_SUSBCRIPTION = "Error en el procesamiento de la suscripcion, intente más tarde"
        valid_instances = Instance.objects.filter(published=True)
        print(valid_instances)

        # instance = Instance.objects.get(name='Proceso de Titulación primavera 2021')
        # target = SubscriptionLink.Destiny.TO_STEPS
        # chat = tg_id['chat_id']
        # user = tg_id['id']

        # if target is None:
        # target = SubscriptionLink.Destiny.TO_STEPS

        # try:
        #     link = SubscriptionLink.objects.get(instance=instance,destiny=target)
        # except:
        #     link = SubscriptionLink()
        #     link.instance = instance
        #     link.destiny = target
        #     link.save() 
        # try:
        #     new_user = BotUser.objects.get(uid=user)
        #     try:
        #         new_settings = BotUserPermissions.objects.get(user=new_user)
        #     except:
        #         new_settings = BotUserPermissions()
        #         new_settings.user = new_user
        #         new_settings.identity = True
        #         new_settings.subscriptions = True
        #         new_settings.save()
        # except Exception as e:
        #     try:
        #         new_user = BotUser(uid=user)
        #         new_user.save()
        #         new_settings = BotUserPermissions()
        #         new_settings.user = new_user
        #         new_settings.identity = True
        #         new_settings.subscriptions = True
        #         new_settings.save()
        #     except Exception as e1:
        #         return ERR_USER
        # try:
        #     print(new_user)
        #     try:
        #         new_subscription = new_subscription = Subscription.objects.get(bot_user=new_user, target_element=link)
        #     except:
        #         frequency = datetime.timedelta(minutes=3) #(days=20, hours=10)
        #         new_subscription = Subscription(bot_user=new_user, chat = chat, target_element=link, frequency=frequency)
        #         new_subscription.save()
        #         new_subscription = Subscription.objects.get(bot_user=new_user, target_element=link)

        #             #   Save Notification
        #         notification = Notification()
        #         notification.subscription = new_subscription
        #         notification.msg = get_notification_test()
        #         notification.next_notification = tz.now() + new_subscription.frequency
        #         notification.save()
        #     message = markup_clearner(f'Nueva suscripción {new_subscription}')
        # except Exception as e:
        #     print(e)
        #     message = ERR_SUSBCRIPTION
        
        # return message