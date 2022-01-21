import re
from ..command import Command


class NotificationCommand(Command):
    name = '/notifications'
    re = re.compile(r'\/notifications')

    @property
    def response(self):
        pass