from enum import Enum
import re
import json
from telegram.Handlers import  (
    CommandHandler,
    LabelHandler
)


class Expressions():
    """Expressions in telegram valid updates
    that can be recognizes by this bot.
    They are stored as python regular expresions
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

    @staticmethod
    def get_user_message_fields(update):
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
    def get_user_callback_query(update):
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
    """Decodes updates and expresions contains in the updates
    """
    command_handler = CommandHandler()
    label_handler = LabelHandler()

    def parse_expression(self, expresion):
        """take a telegram expresion in message
        o callback query data and parse it
        when recognize it, derives to a handler, then
        the handler with create the apropiate expresion
        and call its acction

        Args:
            expresion (json): a telegram api update object
        """
        if Expressions.command.match(expresion) is not None:
            self.command_handler.handle(expresion)

        elif Expressions.label.match(expresion) is not None:
            self.label_handler.handle(expresion)
    
    def decode_update(self, updates):
        """get a telegram message and regonize the
        currently supported types

        Args:
            update (json): a telegram update object
        """
        if Updates.user_message.search(updates) is not None:
            return Updates.get_user_message_fields(updates)

        elif Updates.user_callback_query.search(updates) is not None:
            return Updates.get_user_callback_query(updates)