from .base import TelegramObject

class InlineKeyboardButton(TelegramObject):
    text : str
    url : str
    login_url : str
    callback_data : str
    switch_inline_query : str
    switch_inline_query_current_chat : str
    callback_game : str
    pay : str
    

class InlineKeyboardMarkup(TelegramObject):
    inline_keyboard : list[list[InlineKeyboardButton]]