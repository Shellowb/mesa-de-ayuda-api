from abc import ABC, abstractmethod
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
    __re_name : str # r'\/command'
    __action : function
    keyboard : Keyboard

    @abstractmethod
    def do_action(self, *args, **kwargs):
        return self.__action(*args, **kwargs)

    @property
    @abstractmethod
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = str(new_name)
    
    @property
    @abstractmethod
    def re(self):
        return self.__re_name

    @property
    @abstractmethod
    def response(self) -> dict:
        _response = { 'text' : None, 'keyboard' : self.keyboard}

class StartCommand(Command):
    name = '/start'
    re_name = r'\/start'

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
    keyboard = self.get_process_keyboard

class SettingsCommand(Command):
    msg = BotUserPermissions.set_permissions(user_id=t_chat,id=True, sub=True, sup=True)
    print(msg)
    msg = markup_clearner(msg)
    messages = [
        {"text": msg, "keyboard": {}}
    ]

class FAQCommand(Command):
    message = f'Actualmente puedo ayudarte con /preguntasFrecuentes de...'
    keyboard = None

class SubscriptionCommand(Command):
    msg = ""
    for choice in SubscriptionLink.Destiny.choices:
        msg += f'{choice[0]} {choice[1]}\n'
    # for instance in Instance.objects.all
    messages = [
        {"text": msg, "keyboard": {}}
        ]
    msg = subscribe(t_chat,t_chat,1)

class NotificationCommand(Command):
      send_today_notifications()
    send_today_notifications.delay()
    add.delay(4,4)
    messages = [
        {"text": 'notf', "keyboard": {}}
    ]

class AssistantCommand(Command):
    message = f'Okey, te contactare con un@ asistente. Por favor ingresa tu consulta acontinuación'

class HelpCommand(Command):
    pass