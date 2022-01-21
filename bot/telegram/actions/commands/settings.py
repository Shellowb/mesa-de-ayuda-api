from ctypes import BigEndianStructure
from pyexpat.errors import messages
import re as regex
from ..command import Command
from botUsers.models import BotUser, BotUserPermissions
from bot.telegram.connection import send_message

class SettingsCommand(Command):
    name = '/settings'
    re = regex.compile(r'\/settings\s*(help)*')
    re_help = regex.compile(r'\/settings\shelp')
    re_enable = regex.compile(r'\/settings\senable')
    re_disable = regex.compile(r'\/settings\sdisable')
    re_identity = regex.compile(r'\/settings\sidentity\s')
    re_subscriptions = regex.compile(r'\/settings\ssubscriptions\s')
    re_support_contact = regex.compile(r'\/settings\ssupport_contact\s')
    re_true = regex.compile(r'(T|t)(R|r)(U|u)(E|e)')
    re_false = regex.compile(r'(F|f)(A|a)(L|l)(S|s)(E|e)')

    def do_action(
        self,
        chat_id=None,
        expression=None,
        *args, **kwargs):

        ERR_SETUP = 'El valor que enviaste no se pudo procesar como True o False'

        if expression is not None:
            # expression ~ /settings help
            if self.re_help.match(expression):
                send_message(self.help['text'], chat_id, keyboard=self.help['keyboard'])

            # expression ~ /settings enable
            elif self.re_enable.match(expression):
                msg = BotUser.create_bot_user(chat_id)
                user = BotUser.get_bot_user(chat_id)
                if user is not None:
                    msg2 = BotUserPermissions.create_permissions(user)
                    send_message(msg2, chat_id, keyboard={})
                send_message(msg, chat_id, keyboard={})
                
            # expression ~ /settings disable
            elif self.re_disable.match(expression):
                msg = BotUser.delete_bot_user(chat_id)
                send_message(msg, chat_id, keyboard={})

            # expression ~ /settings identity value
            elif self.re_identity.match(expression):
                _, value= self.re_identity.split(expression)
                value = self.toBool(value)
                if value is not None:
                    BotUserPermissions.set_permissions(chat_id, id=value)
                    send_message(f'Permisos Actualizados', chat_id, keyboard={})
                else:
                    send_message(ERR_SETUP, chat_id, keyboard={})
                
            # expression ~ /settings subscription value
            elif self.re_subscriptions.match(expression):
                _, value= self.re_subscriptions.split(expression)
                value = self.toBool(value)
                if value is not None:
                    BotUserPermissions.set_permissions(chat_id, sub=value)
                    send_message(f'Permisos Actualizados', chat_id, keyboard={})
                else:
                    send_message(ERR_SETUP, chat_id, keyboard={}) 

            # expression ~ /settings support_user value
            elif self.re_support_contact.match(expression):
                _, value= self.re_support_contact.split(expression)
                value = self.toBool(value)
                if value is not None:
                    BotUserPermissions.set_permissions(chat_id, sup=value)
                    send_message(f'Permisos Actualizados', chat_id, keyboard={})
                else:
                    send_message(ERR_SETUP, chat_id, keyboard={}) 
            
            else:
                for msg in self.response(chat_id):
                    send_message(msg['text'], chat_id, keyboard=msg['keyboard'])  

    def response(self, chat_id):
        permissions = BotUserPermissions.get_permissions(chat_id)
        permissions_dict = {
            True : 'Permitido',
            False: 'Deshabilitado'
        }
        if permissions is not None:
            msg_permissions =(
                'Tus permisos tienen los siguientes valores'
                f'\nid: {permissions_dict[permissions.identity]}'
                f'\nsubscriptions: {permissions_dict[permissions.subscriptions]}'
                f'\nsupport contact: {permissions_dict[permissions.support_contact]}'
            )
        else:
            msg_permissions =  (
                'Tienes todos tus permisos deshabilitados'
                f'\nid: Deshabilitado'
                f'\nsubscriptions: Deshabilitado'
                f'\nsupport contact: Deshabilitado'
            )

        messages = [
            {
                'text': msg_permissions,
                'keyboard': {}
            } 
        ]
        return messages

    @property
    def help(self) -> str:
        msg_enable_settings = {
            'text' : (
                '`/settings`\n\n'
                '`/settings enable`: habilitar permisos \n'
                '`/settings <permission> value\(True \| False\)`\. modificar un permiso\n'
                '\tEj\: `/settings subscriptions True`'
            ),
            'keyboard': {}
        }
        return msg_enable_settings

    def toBool(self, value:str) -> bool:
        if self.re_true.match(value) is not None:
            return True
        if self.re_false.match(value) is not None:
            return False