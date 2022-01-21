import re
from typing import List, Dict
from .base import Action 
from bot.telegram.connection import send_message


class Command(Action):
    __name : str    # '/command'
    __re_name : re.Pattern # r'\/command'
    __help : str

    def do_action(self, *args, **kwargs):
        chat_id = kwargs['chat_id']
        for msg  in self.response:
          send_message(msg['text'], chat_id, keyboard=msg['keyboard'])  

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
    def response(self) -> List[Dict]:
        return [{ 'text' : '', 'keyboard' : ''}]

    @property
    def help(self) -> str:
        return self.__help

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
            
    keyboard = '{'+'}'
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
        return [{ 'text' : text, 'keyboard' : self.keyboard}]

    def do_action(self, *args, **kwargs):
        return super().do_action(*args, **kwargs)
