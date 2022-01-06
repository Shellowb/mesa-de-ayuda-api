import re
from abc import ABC, abstractmethod
from bot.telegram.utils import get_process_keyboard
from bot.telegram.connection import send_message
from django.http import response
from botUsers.models import (
    BotUser,
    BotUserPermissions
)


class Keyboard(ABC):
    text : str
    callback_data : dict
    label : str

    @property
    @abstractmethod
    def inline_keyboard(self):
        keyboard = {
            'text' : self.text,
            'callback_data' : self.callback_data,
            'label': self.label
        }
        return {"inline_keyboard": keyboard}

class Command(ABC):
    ERR_INVALID = f'Error invalid Command '
    __name : str    # '/command'
    __re_name : re.Pattern # r'\/command'
    __keyboard : Keyboard

    @abstractmethod
    def do_action(self, *args, **kwargs):
        return

    @property
    @abstractmethod
    def name(self):
        return self.__name

    @name.setter
    @abstractmethod
    def name(self, new_name):
        self.__name = str(new_name)
    
    @property
    @abstractmethod
    def re(self) -> re.Pattern:
        return self.__re_name

    @property
    @abstractmethod
    def response(self) -> dict:
        return { 'text' : None, 'keyboard' :  None}

class StartCommand(Command):
    class StartKeyboard(Keyboard):
        def inline_keyboard(self):
            keyboard_json = get_process_keyboard()
            self.text = keyboard_json['inline_keyboard']['text']
            self.label = keyboard_json['inline_keyboard']['label']
            self.callback_data = keyboard_json['inline_keyboard']['callback_data']
            return keyboard_json

    __name = '/start'
    __re = re.compile(r'\/start')
    __keyboard = StartKeyboard()

    
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name
    
    @property
    def re(self) -> re.Pattern:
        return self.__re

    def do_action(self, *args, **kwargs):
        chat_id = kwargs['chat_id']
        responses = self.response
        for res in responses:
            send_message(res['text'], chat_id, keyboard_button=res['keyboard'])

    @property
    def response(self) :
        link_mesa_de_ayuda = 'https://mesadeayuda.cadcc.cl'
        welcome_message =  (
            f'Hola, soy **Turing** y estoy aqui para ayudarte con tus procesos académicos.\n'
            f'Actualmente te puedo ayudar con consultas, recordatorios o faq par los'
            f'siguientes procesos:'
        )
        dont_forget_message = (
            f'__Recuerda que puedes obtener mas información sobre la mesa de ayuda DCC'
            f'en [mesadeayuda\.cl]({link_mesa_de_ayuda})'
            f'En caso de no poder contestar tu consulta, puedo contactar a un'
            f' /asistente por este mismo canal__'
        )
        responses = [
              { 'text' : welcome_message, 'keyboard' : self.__keyboard.inline_keyboard}
            , { 'text' : dont_forget_message, 'keyboard' : ''}
        ]
        return responses


# class SettingsCommand(Command):
#     msg = BotUserPermissions.set_permissions(user_id=t_chat,id=True, sub=True, sup=True)
#     print(msg)
#     msg = markup_clearner(msg)
#     messages = [
#         {"text": msg, "keyboard": {}}
#     ]

# class FAQCommand(Command):
#     message = f'Actualmente puedo ayudarte con /preguntasFrecuentes de...'
#     keyboard = None

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

# class AssistantCommand(Command):
#     message = f'Okey, te contactare con un@ asistente. Por favor ingresa tu consulta acontinuación'

# class HelpCommand(Command):
#     pass