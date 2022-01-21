from dataclasses import fields
import json
from traceback import print_tb
from typing import Dict, List, NewType, Type, TypedDict
from collections.abc import Sequence

ValidFields = dict[str, type]

class TelegramObject:
    """A Generic Telegram Object
    """
    __fields : TypedDict
    __extended_fields: dict
    # __valid_fields : ValidFields
    __default_encoded_types = [str, int, float]

    def __init__(self, *args, **kwargs):
        self.__fields = {}
        self.__extended_fields = {}

        # Validate field type and name
        for key, value in kwargs.items():
            self.fields[key] = value
        
        # Extend the field to a jsonEncoder default type
        for key, value in self.fields.items():
            if type(value) in self.__default_encoded_types:
                self.__extended_fields[key] = value
            else:
                self.__extended_fields[key] = str(value)
    
    def __getitem__(self, key):
        return self.fields[key]

    def __setitem__(self, key, value):
    
        # if not self.is_valid_key(key):
        #     raise AttributeError(f'the parameter {key} is not a valid InlineKeyboardButton field')

        # if not self.match_types(key, value):
        #     raise TypeError(f'the parameter {key} is not a valid {self.valid_fields[key]}')
        
        self.fields[key] = value

        if type(value) in self.__default_encoded_types: 
            self.__extended_fields[key] = value
        else:
            self.__extended_fields[key] = str(value)

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, new_fields):
        self.__fields = new_fields

    def __str__(self):
        return json.dumps(self.__extended_fields, separators=(',', ':'))     
    
    def __repr__(self) -> str:
        return json.dumps(self.__extended_fields, separators=(',', ':'))


if __name__ == '__main__':


    class InlineKeyboardButton(TelegramObject):
        class Fields(TypedDict):
            text : str
            url : str
            login_url : str
            callback_data : str
            switch_inline_query : str
            switch_inline_query_current_chat : str
            callback_game : str
            pay : str
        fields = Fields()

    class InlineKeyboardMarkup(TelegramObject):

        class Fields(TypedDict):
            inline_keyboard : list[list[InlineKeyboardButton]]
        fields = Fields()

        # def __str__(self):
        #     for l in fields['inline_keyboard']:
        #         for l in fields
        
        
    button = InlineKeyboardButton(
        text="hola",
        url="https://www.google.com"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])

    print(button['text'])
    print(button['url'])
    print(button)
    print(str([[button]]))
    print(keyboard)

    class TlgObj(TypedDict): pass

    class Button(TlgObj):
            text : str
            url : str
            login_url : str
            callback_data : str
            switch_inline_query : str
            switch_inline_query_current_chat : str
            callback_game : str
            pay : str

    class Keyboard(TlgObj):
        inline_keyboard : list[list[Button]]


    button = Button(
        text="process 1",
        callback_data= "id: 1 , label: Process"
    )
    keyboard = Keyboard(inline_keyboard=[[button]])

    print(button)
    print(keyboard)
    print(json.dumps(keyboard, separators=(',', ':')))