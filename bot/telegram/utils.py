import json
from process.models import Process
from process.serializers import ProcessSerializer
from .objects.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
  
def get_process_keyboard(dumped=False) -> InlineKeyboardMarkup or str:
    processes = Process.objects.filter(published=True).order_by('-created_at')
    processes_serializer = ProcessSerializer(processes, many=True)
    buttons = [
        InlineKeyboardButton(
                text=process['name'],
                callback_data = f'id:{process["id"]}, "label": "Process"'
            )
     for process in processes_serializer.data]

    if dumped:
        return json.dumps(InlineKeyboardMarkup(inline_keyboard=[buttons]), separators=(',', ':'))

    return InlineKeyboardMarkup(inline_keyboard=[buttons])

