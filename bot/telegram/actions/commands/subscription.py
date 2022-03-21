from datetime import timedelta
import re as regex
from celery import shared_task
from instances.models import Instance
from botUsers.models import BotUser, BotUserPermissions
from content.models import Subscription, SubscriptionOption
from bot.telegram.actions.command import Command
from bot.telegram.utils import send_message, markdown_cleaner

class SubscriptionCommand(Command):
    name = '/subscription'
    re = regex.compile(r'\/subscription')
    re_help = regex.compile(r'\/subscription help')
    re_options = regex.compile(r'\/subscription\soptions')
    re_c = regex.compile(r'\/subscription\s')
    re_create = regex.compile(r'\/subscription\s\".*\":\".*\"')
    re_create_divider = regex.compile(r':')
    re_available = regex.compile(r'\/subscription\ssubscribed')

    DEFAULT_SUBSCRIPTION_FREQUENCY = timedelta(minutes=1)

    help = (
        f'`\/subscription`\n'
        f'`\/subscription help`\n'
        f'`\/subscription options`\n'
    )

    def do_action(self, chat_id=None, expression=None, *args, **kwargs):
        """"""
        if expression is not None:
            # expression <-> /subscription help
            if self.re_help.match(expression):
                send_message(self.help, chat_id, keyboard_button={})
            
            # expression <-> /subscription options
            elif self.re_options.match(expression):
                send_message(self.options_txt, chat_id, {})
            
            # expression <-> /subscription "Process Name":"Target Name"
            elif self.re_create.match(expression):
                _, value = self.re_c.split(expression)
                value = value.replace('"', "")
                instance, target = self.re_create_divider.split(value)
                self.suscribe(chat_id, instance, target)

            elif self.re_available.match(expression):
                print("exp -> avilable suscriptions")
                send_message(self.user_subscription(chat_id), chat_id, {})

            else:
                for msg  in self.response:
                    send_message(msg['text'], chat_id, keyboard_button=msg['keyboard'])

    @property
    def response(self):
        return [
            {
                "text": "Para suscribirse a algún proceso usa \/subscription \"\<instancia del proceso\>\":\"\<Link\>\"",
                "keyboard": {}
            }
        ]

    @property
    def options_txt(self):
        available_options = SubscriptionOption.aviable_options(only_published=True)
        text = "*Opciones de Suscripción*\n"
        print(available_options)
        for option in available_options:
            print(option)
        return text

    def is_subscription_enabled(chat_id) -> bool:
        permissions = BotUserPermissions.get_permissions(chat_id)
        if permissions is not None:
            return permissions.subscriptions
        return False

    def user_subscription(self, chat_id) -> str:
        susbscriptions = Subscription.objects.filter(chat=chat_id)
        sus_str = ""
        if susbscriptions.exists():
            for suscription in susbscriptions:
                sus_str += suscription.description
        return markdown_cleaner(sus_str)


    # @shared_task
    def suscribe(self, chat_id, instance: str, target:str):
        ERR_SUSBCRIPTION = "Error en el procesamiento de la suscripcion, intente más tarde"
        ERR_NO_INSTANCE = "La Instancia que estás intentando suscribir no existe o no se encuentra publicada"
        ERR_NO_TARGET = "Esta instancia no tiene la opción indicada, habilitada para subscripción"
        
        # get all published instances and its links
        published_instances = Instance.objects.filter(published=True)
        instance_links = {}
    
        if published_instances.exists(): # chek if there are published instances
            for pinstance in published_instances:
                pinstance_links = self.aviable_links(pinstance)
                if pinstance_links is not None: # if instance has links then saves instance name and a list
                    instance_links[pinstance.name] = pinstance_links # saves all instances links into a list for the instance name (key)
        print(f"/suscribe instances and links {instance_links}")
        
        # makes the match between existing instances and its links
        # and user input
        try:
            # if user target in aviable links for instance user given name
            if target in instance_links[instance]:
                user = BotUser.get_bot_user(chat_id)
                instance = Instance.get_instance_by_name(instance, publish=True)
                destiny = SubscriptionLink.destiny_label_to_value(target)
                link = SubscriptionLink.get_subscription_link(instance, destiny)
                if link is not None:
                    msg = Subscription.create_subscription(
                        user=user,
                        chat=chat_id,
                        target=link,
                        # frequency=self.DEFAULT_SUBSCRIPTION_FREQUENCY
                    )
                    send_message(msg, chat_id, keyboard_button={})

                else:
                    send_message(ERR_SUSBCRIPTION, chat_id, keyboard_button={})
            else:
                # means that the user given target doesnt exist in aviable links
                send_message(ERR_NO_TARGET, chat_id, keyboard_button={})
        except KeyError:
            # means that the user give an instance name that doesn exists in database
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