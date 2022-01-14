from .base import Handler

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
