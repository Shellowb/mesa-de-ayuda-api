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
