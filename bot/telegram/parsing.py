import re
import json
from bot.telegram.handlers.commandHandler import CommandHandler
from bot.telegram.handlers.callbackQueryHandler import LabelHandler
from bot.telegram.handlers.unknown import UnknowExpressionHandler


class Expressions():
    """Expressions in telegram valid updates
    that can be recognizes by this bot.
    They are stored as python regular expressions
    so then can be match again the api response.
    """
    # /command arg1 agr2 ... argn
    command = re.compile(r"\/[a-z]*\s*([a-z]*[A-Z]*[0-9]*\s*)*")
    # LabelName
    label = re.compile(r"([A-Z][a-z]*)")


class Updates():
    """Holds the logic, relative to parse the 
    valid updates that can recive from telegram api.
    There only listed supported types for this bot.
    """
    update_id = re.compile(r'update_id')
    user_message = re.compile(r'message')
    user_callback_query = re.compile(r'callback_query')

    class UpdateProccesingResult:
        recognized : bool
        type : str
        # chat_id = int
        def __init__(self, recognized=False, type=None) -> None:
            self.recognized = recognized
            self.type = type

    @staticmethod
    def get_user_message_fields(update : bytes):
        """if the update is a valid message (review docs
        or telegram api), then extracts chat id and the 
        message text (in the case that were a command,
        will return the complete command and args)

        Args:
            update (json): message response from telegram api

        Returns:
            tuple(int, str): returns chat id and msg text
        """
        fields = json.loads(update)
        try:
            chat_id = fields['message']['chat']['id']
            expression = fields['message']["text"]
            return chat_id, expression
        except Exception as e:
            return None

    @staticmethod
    def get_user_callback_query(update : bytes):
        """if the update is a valid callback query (review 
        docs or telegram api), then extracts chat id, data id
        (kind of text), and label.

        Args:
            update (json): message response from telegram api

        Returns:
            tuple(int, str, str): returns chat id, data text &
                                  label
        """
        fields = json.loads(update)
        try:
            callback_query = fields['callback_query']
            chat_id = callback_query['message']['chat']['id']
            data = json.loads(callback_query['data'])
            text = data['id']
            label = data['label']
            return chat_id, text, label
        except Exception as e:
            return None


class Parser:
    """Decodes updates and expressions contained in the updates
    """
    command_handler = CommandHandler()
    label_handler = LabelHandler()
    unknow_expression_handler = UnknowExpressionHandler()

    def parse_expression(self, expression: str, for_id: int):
        """take a telegram expression in message
        o callback query data and parse it
        when recognize it, derives to a handler, then
        the handler with create the apropiate expression
        and call its acction

        Args:
            expression (json): a telegram api update object
        """
        ERR = "Parsing Expresion Error details:\n %s"
        try:
            if Expressions.command.match(expression) is not None:
                return self.command_handler.handle(expression, for_id)

            elif Expressions.label.match(expression) is not None:
                return self.label_handler.handle(expression, for_id)
            
            else:
                return self.unknow_expression_handler.handle(expression, for_id)
        except Exception as e:
            print(f"{e}")
            return ERR.format("f{e}")
            
    
    def decode_update(self, update: bytes):
        """get a telegram message and regonize the
        currently supported types

        Args:
            update (json): a telegram update object
        """
        
        if Updates.user_message.search(update.decode()) is not None:
            message_fields = Updates.get_user_message_fields(update)
            if message_fields is not None:
                chat_id, expression = message_fields
                self.parse_expression(expression, chat_id)
                return Updates.UpdateProccesingResult(True, Updates.user_message)
            return Updates.UpdateProccesingResult()

        elif Updates.user_callback_query.search(update.decode()) is not None:
            callback_query = Updates.get_user_callback_query(update)
            if callback_query is not None:
                chat_id, text, label = callback_query
                self.parse_expression(label, chat_id)
                return Updates.UpdateProccesingResult(True, Updates.user_callback_query)
            return Updates.UpdateProccesingResult()

        else:
            return Updates.UpdateProccesingResult()