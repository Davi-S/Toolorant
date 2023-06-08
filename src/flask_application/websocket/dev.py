import asyncio
import psutil
from ..abstracts import Publisher
import threading

class WebSocket(Publisher):
    def __init__(self):
        super().__init__()
        self.__observe_running = False
        self.__web_socket_running = False
        self._is_valorant_open = False

    async def _web_socket(self):
        print('starting ws')
        count = 0
        while self.__web_socket_running:
            count += 1
            print(f'ws loop {count}')

            if count in {10, 20, 30}:
                print('ws notifying listeners')
                self.notify_listeners('pregame_started')

            await asyncio.sleep(1)
        print('stopping ws')

    async def _observe(self):
        print('starting observe')
        count = 0
        while self.__observe_running:
            count += 1
            print(f'observe loop {count}')

            # TODO: change program name to the valorant name 'VALORANT-Win64-Shipping.exe'
            current_status = any('notepad.exe' in proc.info['name'].lower()
                                 for proc in psutil.process_iter(['name']))
            if current_status != self._is_valorant_open:
                print('observe event received')
                self._is_valorant_open = current_status
                self._on_program_event(
                    'open' if self._is_valorant_open else 'close')

            await asyncio.sleep(1)
        print('stopping observe')

    def _on_program_event(self, event):
        print(event)
        if event == 'open':
            self.__web_socket_running = True
            threading.Thread(target=self._start_web_socket,
                             args=(), daemon=True).start()
        elif event == 'close':
            self.__web_socket_running = False

    def start(self):
        tr = threading.Thread(target=self._start,
                              args=(), daemon=True)
        tr.start()
        return bool(tr.is_alive())

    def _start(self):
        if self.__observe_running:
            return False
        self.__observe_running = True
        threading.Thread(target=self._start_observe,
                         args=(), daemon=True).start()
        return True

    def stop(self):
        if not self.__observe_running:
            return False
        self.__observe_running = False
        self.__web_socket_running = False
        return True

    def _start_observe(self):
        asyncio.run(self._observe())

    def _start_web_socket(self):
        asyncio.run(self._web_socket())
