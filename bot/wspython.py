import asyncio
import threading
import websockets
import json

class Wspython(threading.Thread):
  async def send_to_websocket(self, chat_id, message):
    async with websockets.connect(f'ws://localhost:8000/ws/chat/{chat_id}/') as websocket:
      try:
        context = json.dumps({"message": message, "bot": True, "command": "new_message"})
        await websocket.send(context)
      except Exception as e:
        print(e)

  def send(self, chat_id, message):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(self.send_to_websocket(chat_id, message))

