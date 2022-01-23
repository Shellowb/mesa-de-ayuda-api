from cmath import exp
from .base import Handler
from bot.telegram.actions.command import Command
from bot.telegram.actions.commands.unknown import UnknownCommand
from bot.telegram.actions.commands.start import StartCommand
from bot.telegram.actions.commands.help import HelpCommand
from bot.telegram.actions.commands.settings import SettingsCommand
from bot.telegram.actions.commands.faq import FAQCommand
from bot.telegram.actions.commands.assitant import AssistantCommand
from bot.telegram.actions.commands.subscription import SubscriptionCommand



class CommandHandler(Handler):
    start_command = StartCommand()
    help_command = HelpCommand()
    unknown_command = UnknownCommand()
    settings_command = SettingsCommand()
    faq_command = FAQCommand()
    assitant_command = AssistantCommand()
    subscription_command = SubscriptionCommand()

    def handle(self, expression: str, for_id: int) -> None:

        # expression <-> /start
        if self.start_command.re.match(expression):
            self.start_command.do_action(chat_id=for_id)

        # expression <-> /help
        elif self.help_command.re.match(expression):
            self.help_command.do_action(chat_id=for_id)

        # expression <-> /settings            
        elif self.settings_command.re.match(expression):
            self.settings_command.do_action(chat_id=for_id, expression=expression)

        # expression <-> /faq       
        elif self.faq_command.re.match(expression):
            self.faq_command.do_action(chat_id=for_id)

        # expression <-> /assistant 
        elif self.assitant_command.re.match(expression):
            self.assitant_command.do_action(chat_id=for_id)
        
        # expression <-> /subscription
        elif self.subscription_command.re.match(expression):
            self.subscription_command.do_action(chat_id=for_id, expression=expression)
            
        else:
           self.unknown_command.do_action(chat_id=for_id)
