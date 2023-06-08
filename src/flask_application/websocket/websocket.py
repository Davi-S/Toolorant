import asyncio
from ..abstracts import Publisher
import threading


class WebSocket(Publisher):
    def __init__(self):
        super().__init__()
        self.__running = False

    async def _web_socket(self, port, password):
        print(f'starting ws with port: {port} and password: {password}')
        count = 0
        while self.__running:
            count += 1
            print(f'ws loop {count}')

            if count in {10, 20, 30}:
                print('notifying listeners')
                self.notify_listeners('pregame_started')
            await asyncio.sleep(1)
        print('stopping ws')

    def start(self, lockfile):
        if self.__running:
            return False
        self.__running = True
        t = threading.Thread(target=self._start, args=(lockfile['port'], lockfile['password']), daemon=True)
        t.start()
        return t.is_alive()
    
    def _start(self):
        asyncio.run(self._web_socket())

    def stop(self):
        if not self.__running:
            return False
        self.__running = False
        return True
    
    def is_running(self):
        return self.__running

    
    