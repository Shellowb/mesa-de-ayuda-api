from abc import ABC, abstractmethod
from bot.telegram.commands import (
    StartCommand
)

class Handler(ABC):
    """Handles an action to be perform
    when a especifici type is recognized in
    parse
    """

    @abstractmethod
    def handle(expression: str, for_id: int) -> None:
        """Handles a expression

        Args:
            expresion (str): a expression to be handled
        """
        pass

class CommandHandler(Handler):
    start_command = StartCommand()

    def handle(self, expression: str, for_id: int) -> None:
        if self.start_command.re.match(expression):
            self.start_command.do_action(chat_id=for_id)


class LabelHandler(Handler):
    label_names = [
            'Process',
            'Category',
            'Question',
            'Feedback',
            'Helper'
        ]
    labels_pattern = r'('+'|'.join(label for label in label_names)+')+'

    def handle(expression: str) -> None:
        return super().handle()