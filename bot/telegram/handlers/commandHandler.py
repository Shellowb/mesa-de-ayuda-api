from .base import Handler
from bot.telegram.actions.commands.start import StartCommand
from bot.telegram.actions.commands.unknown import UnknownCommand
from bot.telegram.actions.command import Command



class CommandHandler(Handler):
    start_command = StartCommand()
    unknown_command = UnknownCommand()
    command : Command

    def handle(self, expression: str, for_id: int) -> None:

        if self.start_command.re.match(expression):
            self.command = self.start_command

        else:
           self.action = self.unknown_command

        self.command.do_action(chat_id=for_id)
