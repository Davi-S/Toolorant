import asyncio
import base64
import enum
import json
import logging
import ssl
import threading

import websockets
import websockets.exceptions

from abstracts import Publisher


logger = logging.getLogger(__name__)


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

        async with websockets.connect(
            f"wss://127.0.0.1:{port}",
            ssl=ssl_context,
            extra_headers={
                'Authorization': f"Basic {base64.b64encode(f'riot:{password}'.encode()).decode()}"
            }
        ) as websocket:
            await websocket.send('[5, "OnJsonApiEvent"]')
            logger.info('Websocket connection started. Getting responses...')
            while True:
                try:
                    response = await websocket.recv()
                    response = json.loads(response)[2]
                except websockets.exceptions.ConnectionClosedError as e:
                    self.is_running = False
                    logger.warning('Websocket connection closed')
                    return
                except json.decoder.JSONDecodeError:
                    # Because of empty response
                    continue

                for event in Event:
                    if event.value in response['uri']:
                        logger.info(f'Important response received: {event.name}')
                        # Call the listeners on another thread so the ws thread is always running without interruption
                        # Important: There will be multiple calls to the same event in a short period of time because of how the Valorant API works and how we identify the events/responses
                        threading.Thread(
                            target=self.notify_listeners,
                            name='WSNotifyListeners',
                            args=(event,),
                            daemon=True
                        ).start()

    def _start(self, port, password):
        asyncio.run(self._web_socket(port, password))
        
    def start(self, port, password):
        if self.is_running:
            logger.debug('Websocket is already running')
            return False
        self.is_running = True
        threading.Thread(
            target=self._start,
            name='WSThread',
            args=(port, password),
            daemon=True
        ).start()
        logger.debug('Websocket started successfully')
        return True

    def stop(self):
        if not self.is_running:
            logger.debug('Websocket is already stopped')
            return False
        self.is_running = False
        logger.debug('Websocket stopped successfully')
        return True
