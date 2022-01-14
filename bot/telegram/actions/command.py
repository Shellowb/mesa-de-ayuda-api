import re
from typing import List, Dict
from .base import Action 
from bot.telegram.objects.keyboard import Keyboard
from bot.telegram.connection import send_message


class Command(Action):
    __name : str    # '/command'
    __re_name : re.Pattern # r'\/command'
    __keyboard : Keyboard

    def do_action(self, *args, **kwargs):
        chat_id = kwargs['chat_id']
        new_messages = self.response()
        for msg  in new_messages:
          send_message(msg['text'], chat_id, keyboard_button=msg['keyboard'])  

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
