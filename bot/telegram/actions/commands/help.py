import re
from ..command import Command

class HelpCommand(Command):
    name = '/help'
    re = re.compile(r'\/help')

    @property
    def response(self) :
        welcome_message =  (
            f'''
            Una Manita\?
            Soy un bot pensado para asistirte en tus procesos académicos\.
            Para eso tengo tres modalidades de uso\:
            '''
        )
        msg2 = (
            f'''
            *1\. Flujo desde Start\:* Si envías el comando /start, yo te iré guiando
            por mis distintas funcionalidades\, es cómodo si no quieres recordar
            todo lo que puedo hacer\, y en general deberías llegar rápido a cualquier
            funcionalidad que yo tenga disponible\.
            '''
        )
        msg3 = (
            f'''
            *2\. Commandos\:* Si ya sabes lo que quieres cool\, mandame una request personalizada
            con un comando\. Algunos comandos aceptan parametros\. Te los listo a continuación\:
            ```
            - /help
            - /start
            - /settings
            - /notification
            ```
            '''
        )

        msg4 = (
            f'''*lista de comandos*
            /help
            /start
            /settings
            /notification
            /subscription
            /faq
            '''
        )
        msg5 = (
            f'''
            *3. Preguntas Mapeadas y no mapeadas*
            '''
        )
       

        mesages = [
              { 'text' : welcome_message, 'keyboard' : {}}
              , { 'text' : msg2, 'keyboard' : {}}
              , { 'text' : msg3, 'keyboard' : {}}
              , { 'text' : msg4, 'keyboard' : {}}
              , { 'text' : msg5, 'keyboard' : {}}
        ]

        return mesages
