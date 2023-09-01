import asyncio
import base64
import enum
import logging
import ssl
import threading

import websockets
import websockets.exceptions

from logging_configuration import create_file_handler

from ..abstracts import Publisher


# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))

class Event(enum.Enum):
    PREGAME = "/riot-messaging-service/v1/message/ares-pregame/pregame/v1/matches/"


class WebSocket(Publisher):
    def __init__(self):
        super().__init__()
        self.is_running = False

    async def _web_socket(self, port, password):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with websockets.connect(f"wss://127.0.0.1:{port}",
                                      ssl=ssl_context,
                                      extra_headers={'Authorization': f"Basic {base64.b64encode(f'riot:{password}'.encode()).decode()}"}) as websocket:
            await websocket.send('[5, "OnJsonApiEvent"]')
            log.info('Websocket connection started. Getting responses...')
            while True:
                try:
                    response = await websocket.recv()
                except websockets.exceptions.ConnectionClosedError as e:
                    self.is_running = False
                    return
                
                for event in Event:
                    if event.value in response:
                        log.info(f'Important response received ({event.name}): """{response}"""')
                        # Call the listeners on another thread so the ws thread is always running without interruption
                        # TODO: Fix notify_listeners can be called multiple times for the same event
                        threading.Thread(target=self.notify_listeners, args=(event,), daemon=True).start()

    def start(self, lockfile):
        if self.is_running:
            log.debug('Failed to start. Websocket is already running')
            return False
        self.is_running = True
        t = threading.Thread(target=self._start,
                             args=(lockfile['port'], lockfile['password']),
                             daemon=True,
                             name='WSThread')
        t.start()
        log.debug('Websocket thread started successfully')
        return t.is_alive()

    def _start(self, port, password):
        asyncio.run(self._web_socket(port, password))

    def stop(self):
        if not self.is_running:
            log.debug('Failed to stop. Websocket is already stopped')
            return False
        self.is_running = False
        log.debug('Websocket stopped successfully')
        return True
