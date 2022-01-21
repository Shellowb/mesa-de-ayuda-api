import re
from ..command import Command

class AssistantCommand(Command):
    name = '/asistente'
    re = re.compile(r'\/asistente')
    @property
    def response(self) :
        message = f'Okey\, te contactare con un@ asistente\. Por favor ingresa tu consulta acontinuación'
        return [{ 'text' : message, 'keyboard' : {}}]