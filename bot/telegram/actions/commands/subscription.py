from datetime import timedelta
import re as regex
from celery import shared_task
from instances.models import Instance
from botUsers.models import BotUser, BotUserPermissions, SubscriptionLink, Subscription
from bot.telegram.actions.command import Command
from bot.telegram.utils import send_message

class SubscriptionCommand(Command):
    name = '/subscription'
    re = regex.compile(r'\/subscription')
    re_help = regex.compile(r'\/subscription help')
    re_options = regex.compile(r'\/subscription\soptions')
    re_c = regex.compile(r'\/subscription\s')
    re_create = regex.compile(r'\/subscription\s\".*\":\".*\"')
    re_create_divider = regex.compile(r':')

    DEFAULT_SUBSCRIPTION_FREQUENCY = timedelta(minutes=1)

    help = (
        f'`subscription`\n'
        f'asjdaksjdajks'
    )

    def do_action(
        self,
        chat_id=None,
        expression=None,
        *args, **kwargs):

        if expression is not None:
            # expression <-> /subscription help
            if self.re_help.match(expression):
                send_message(self.help, chat_id, keyboard_button={})
            
            # expression <-> /subscription options
            elif self.re_options.match(expression):
                send_message(self.options, chat_id, {})
            
            # expression <-> /subscription "Process Name":"Target Name"
            elif self.re_create.match(expression):
                _, value = self.re_c.split(expression)
                value = value.replace('"', "")
                instance, target = self.re_create_divider.split(value)
                self.suscribe(chat_id, instance, target)

            else:
                for msg  in self.response:
                    send_message(msg['text'], chat_id, keyboard_button=msg['keyboard'])

    @property
    def response(self):
        return [
            {
                "text": " Subscription defatult response",
                "keyboard": {}
            }
        ]

    @property
    def options(self):
        instances = Instance.objects.filter(published=True)
        available_links = []
        print(instances)
        for instance in instances:
                instance_available_links = self.aviable_links(instance)
                print(instance_available_links)
                if instance_available_links is not None:
                    for instance_link in instance_available_links:
                        available_links.append(
                            (instance.name, instance_link)
                        )
        text = "*Opciones de Suscripción*\n"
        for link in available_links:
            text += f'{link[0]}:{link[1]}\n'
        return text

    def is_subscription_enabled(chat_id) -> bool:
        permissions = BotUserPermissions.get_permissions(chat_id)
        if permissions is not None:
            return permissions.subscriptions
        return False

    def aviable_links(self, instance: Instance) -> list[str]:
        links = SubscriptionLink.objects.filter(instance=instance)
        labels = []
        if links.exists():
            for link in links:
                labels.append(link.destiny_label)
            return labels
        return None

    # @shared_task
    def suscribe(self, chat_id, instance: str, target:str):
        ERR_SUSBCRIPTION = "Error en el procesamiento de la suscripcion, intente más tarde"
        ERR_NO_INSTANCE = "La Instancia que estás intentando suscribir no existe o no se encuentra publicada"
        ERR_NO_TARGET = "Esta instancia no tiene la opción indicada, habilitada para subscripción"
        valid_instances = Instance.objects.filter(published=True)
        links = {}
        for vinstance in valid_instances:
            vinstance_links = self.aviable_links(vinstance)
            if vinstance_links is not None:
                links[vinstance.name] = []
            for vi_link in vinstance_links:
                links[vinstance.name].append(vi_link)
        print(links)
        try:
            if target in links[instance]:
                user = BotUser.get_bot_user(chat_id)
                instance = Instance.get_instance_by_name(instance, publish=True)
                destiny = SubscriptionLink.destiny_label_to_value(target)
                link = SubscriptionLink.get_subscription_link(instance, destiny)
                if link is not None:
                    msg = Subscription.create_subscription(
                        user=user,
                        chat=chat_id,
                        target=link,
                        frequency=self.DEFAULT_SUBSCRIPTION_FREQUENCY
                    )
                    send_message(msg, chat_id, keyboard_button={})

                else:
                    send_message(ERR_SUSBCRIPTION, chat_id, keyboard_button={})
            else:
                send_message(ERR_NO_TARGET, chat_id, keyboard_button={})
        except KeyError:
            send_message(ERR_NO_INSTANCE, chat_id, keyboard_button={})
        

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