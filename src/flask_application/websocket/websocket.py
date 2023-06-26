import asyncio
import enum
import json
from ..abstracts import Publisher
import threading
import ssl
import websockets
import base64

class Event(enum.Enum):
    PREGAME = "/riot-messaging-service/v1/message/ares-pregame/pregame/v1/matches/"

class WebSocket(Publisher):
    def __init__(self):
        super().__init__()
        self.__running = False

    async def _web_socket(self, port, password):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with websockets.connect(f"wss://127.0.0.1:{port}", ssl=ssl_context,
                                      extra_headers={'Authorization': f"Basic {base64.b64encode(f'riot:{password}'.encode()).decode()}"}) as websocket:

            await websocket.send('[5, "OnJsonApiEvent"]')

            while True:
                response = await websocket.recv()
                for event in Event:
                    if event.value in response:
                        # Call the listeners on another thread so the ws thread is always running without interruption
                        # TODO: Fix the following problem: notify_listeners can be called multiple times for the same event
                        threading.Thread(target=self.notify_listeners, args=(event,), daemon=True).start()
                
                # with open('logs\event_logs.json', 'a') as f:
                #     json.dump(json.loads(response)[2], f, indent=4)

    def start(self, lockfile):
        if self.__running:
            return False
        self.__running = True
        t = threading.Thread(target=self._start, args=(lockfile['port'], lockfile['password']), daemon=True)
        t.start()
        return t.is_alive()
    
    def _start(self, port, password):
        asyncio.run(self._web_socket(port, password))

    def stop(self):
        if not self.__running:
            return False
        self.__running = False
        return True
    
    def is_running(self):
        return self.__running

    
    