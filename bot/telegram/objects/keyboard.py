import json

class Keyboard:
    __text : str
    __callback_data : dict
    __label : str

    @property
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, new_text:str):
        self.__text = new_text

    @property
    def callback_data(self) -> dict:
        return self.__callback_data

    @callback_data.setter
    def callback_data(self, new_callback_data: dict):
        self.__callback_data = new_callback_data

    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, new_label:str):
        self.__label = new_label

    @property
    def inline_keyboard(self) -> str:
        keyboard = {
            "inline_keyboard" : { 
                'text' : self.text,
                'callback_data' : self.callback_data,
                'label': self.label
            }
        }
        return json.dumps(keyboard, separators=(',', ':'))