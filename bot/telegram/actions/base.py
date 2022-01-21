from abc import ABC, abstractmethod
from bot.telegram.connection import send_message

class Action(ABC):

    @abstractmethod
    def do_action(self, *args, **kwargs):
        pass


class CatchUnknownExpression(Action):
    ERR_UNDECODED = f'El mensaje recibido se enviará a un asistente'
    def do_action(self, *args, **kwargs):
        chat_id = kwargs['chat_id']
        send_message(self.ERR_UNDECODED, chat_id, keyboard='{'+'}')
        


# class SubscriptionCommand(Command):
#     msg = ""
#     for choice in SubscriptionLink.Destiny.choices:
#         msg += f'{choice[0]} {choice[1]}\n'
#     # for instance in Instance.objects.all
#     messages = [
#         {"text": msg, "keyboard": {}}
#         ]
#     msg = subscribe(t_chat,t_chat,1)

# class NotificationCommand(Command):
#     send_today_notifications()
#     send_today_notifications.delay()
#     add.delay(4,4)
#     messages = [
#         {"text": 'notf', "keyboard": {}}
#     ]

