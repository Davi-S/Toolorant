import asyncio
from ...observer_pattern_abstract import Publisher
import enum


class Event(enum.Enum):
    PREGAME_STARTED = enum.auto()
    

class WebSocket(Publisher):
    def __init__(self):
        super().__init__()
        self.__running = False

    async def _web_socket(self):
        print('starting ws')
        count = 0
        while self.__running:
            count += 1
            print('websocket loop')
            await asyncio.sleep(1)

            # TODO: implement how to proceed when the match is found
            if count in {10, 20, 30}:
                print('notifying listeners')
                self.notify_listeners(Event.PREGAME_STARTED)
        print('stopping ws')

    def start(self):
        if self.__running:
            return
        self.__running = True
        asyncio.run(self._web_socket())

    def stop(self):
        if not self.__running:
            return
        self.__running = False
