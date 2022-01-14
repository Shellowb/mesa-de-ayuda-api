import re
import json
from typing import Dict, List

from django.utils.translation import override


class Keyboard:
    __text : str
    __callback_data : dict
    __label : str

    @property
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, new_text:str):
        self.__text = new_text

    @property
    def callback_data(self) -> dict:
        return self.__callback_data

    @callback_data.setter
    def callback_data(self, new_callback_data: dict):
        self.__callback_data = new_callback_data

    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, new_label:str):
        self.__label = new_label

    @property
    def inline_keyboard(self) -> str:
        keyboard = {
            "inline_keyboard" : { 
                'text' : self.text,
                'callback_data' : self.callback_data,
                'label': self.label
            }
        }
        return json.dumps(keyboard, separators=(',', ':'))


class Command:
    __name : str    # '/command'
    __re_name : re.Pattern # r'\/command'
    __keyboard : Keyboard

    def do_action(self, *args, **kwargs):
        # chat_id = kwargs['chat_id']
        # new_messages = self.response()
        # for msg  in new_messages:
        #   send_message(msg['text'], chat_id, keyboard_button=msg['keyboard'])  
        pass

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = str(new_name)
    
    @property
    def re(self) -> re.Pattern:
        return self.__re_name
    
    @re.setter
    def re(self, new_re):
        self.__re_name = new_re

    @property
    def keyboard(self) -> Keyboard:
        return self.__keyboard

    @keyboard.setter
    def keyboard(self, new_keyboard:Keyboard):
        self.__keyboard = new_keyboard

    @property
    def response(self) -> List[Dict]:
        return [{ 'text' : 'None', 'keyboard' : self.__keyboard}]


class StartCommand(Command):
    class StartKeyboard(Keyboard):
        @property
        def inline_keyboard(self):
            # keyboard = get_process_keyboard()
            # self.text = keyboard['inline_keyboard'][0][0]['text']
            # self.label = keyboard['inline_keyboard'][0][0]['label']
            # self.callback_data = keyboard['inline_keyboard'][0][0]['data']
            return {}

    name = '/start'
    re = re.compile(r'\/start')
    Keyboard = StartKeyboard()

    def do_action(self, *args, **kwargs):
        return super().do_action(*args, **kwargs)

    @property
    def response(self) :
        link_mesa_de_ayuda = 'https://mesadeayuda.cadcc.cl'
        welcome_message =  (
            f'Hola, soy *Turing* y estoy aqui para ayudarte con tus procesos académicos \.\n'
            f'Actualmente te puedo ayudar con consultas, recordatorios o faq par los '
            f'siguientes procesos'
        )
        dont_forget_message = (
            f'_Recuerda que puedes obtener mas información sobre la mesa de ayuda DCC '
            f'en [mesadeayuda\.cl]({link_mesa_de_ayuda}) '
            f'En caso de no poder contestar tu consulta, puedo contactar a un'
            f' \/asistente por este mismo canal_'
        )
        responses = [
              { 'text' : welcome_message, 'keyboard' : self.__keyboard.inline_keyboard}
            , { 'text' : dont_forget_message, 'keyboard' : {}}
        ]
        return responses


class NotDefinedCommand(Command):
    """[summary]

    Args:
        Command ([type]): [description]

    Returns:
        [type]: [description]
    """
    class CommandError:
        error : str
        
        def __init__(self, error=None):
            if error is None:
                self.error = ''
            else:
                self.error = error

        def __str__(self):
            return self.error
            
    class EmptyKeyboard(Keyboard):

        @property
        def inline_keyboard(self):
            return '{'+'}'

    keyboard = EmptyKeyboard()
    __error : CommandError

    @property
    def error(self) -> CommandError:
        self.__error
    
    @error.setter
    def error(self, new_error : CommandError):
        self.__error = new_error

    @property
    def response(self) -> List[Dict]:
        text = str(self.error)
        return [{ 'text' : text, 'keyboard' : self.keyboard.inline_keyboard}]

    def do_action(self, *args, **kwargs):
        return super().do_action(*args, **kwargs)


class UnknownCommand(NotDefinedCommand):
    ERR_UNKNOWN = f'''El texto que enviaste, 
                    no se reconoce como commando, 
                    le enviaremos tu mensaje a un asistente
                    '''
    error = NotDefinedCommand.CommandError(ERR_UNKNOWN)


class UnDecodedCommand(NotDefinedCommand):
    ERR_UNDECODED = f'El mensaje recibido no se pudo procesar.'
    error = NotDefinedCommand.CommandError(ERR_UNDECODED)