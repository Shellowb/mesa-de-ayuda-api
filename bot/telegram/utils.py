import json
from process.models import Process
from process.serializers import ProcessSerializer

def markup_cleanner(text: str) -> str:
    especial_characters = [
        '_', '*', '[', ']', '(', ')',
        '~', '`', '>', '#', '+', '-',
         '=', '|', '{', '}', '.', '!'
    ]
    for ch in especial_characters:
        text = text.replace( ch , '\\' + ch)
    return text

 
  
def get_process_keyboard():
    processes = Process.objects.filter(published=True).order_by('-created_at')
    processes_serializer = ProcessSerializer(processes, many=True)
    keyboard = [
        [
            {
                  "text": process['name']
                , "callback_data" :
                    json.dumps({
                          "id": str(process['id'])
                        , "label": "Process"
                    }, separators=(',', ':'))
            }
        ] for process in processes_serializer.data  
    ]
    return {"inline_keyboard": keyboard}

