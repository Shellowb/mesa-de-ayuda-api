from abc import ABC, abstractmethod

class Handler(ABC):
    
    @staticmethod
    @abstractmethod
    def parse(something :str) -> None:
        pass

    @staticmethod
    @abstractmethod
    def handle() -> None:
        pass

class CommandHandler(Handler):
    pass

class LabelHandler(Handler):
    label_names = [
            'Process',
            'Category',
            'Question',
            'Feedback',
            'Helper'
        ]
    labels_pattern = r'('+'|'.join(label for label in label_names)+')+'

    