import re
from ..command import Command
from bot.telegram.utils import get_process_keyboard

class FAQCommand(Command):
    name = "/faq"
    re = re.compile(r'(\/faq|\/preguntasFrecuentes)')

    @property
    def response(self) :
        message = f'Actualmente puedo ayudarte con /preguntasFrecuentes de\:'
        mesages = [
              { 'text' : message, 'keyboard' : get_process_keyboard(dumped=True)}
        ]
        return mesages
    