import re
from ..command import Command
from bot.telegram.objects.keyboard import Keyboard
from bot.telegram.utils import get_process_keyboard

class StartCommand(Command):
    class StartKeyboard(Keyboard):
        @property
        def inline_keyboard(self):
            keyboard = get_process_keyboard()
            # self.text = keyboard['inline_keyboard'][0][0]['text']
            # self.label = keyboard['inline_keyboard'][0][0]['label']
            # self.callback_data = keyboard['inline_keyboard'][0][0]['data']
            return {}

    name = '/start'
    re = re.compile(r'\/start')
    Keyboard = StartKeyboard()

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
