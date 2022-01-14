from .base import Handler
from bot.telegram.actions.base import CatchUnknownExpression


class UnknowExpressionHandler(Handler):
    action = CatchUnknownExpression()
    def handle(self, expression: str, for_id: int) -> None:
        self.action.do_action(expression, chat_id=for_id)