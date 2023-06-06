import abc


class Publisher(abc.ABC):
    def __init__(self):
        self._listeners: set[Listener] = set()

    def add_listener(self, listener):
        self._listeners.add(listener)

    def remove_listener(self, listener):
        self._listeners.discard(listener)

    def notify_listeners(self, event):
        for listener in self._listeners:
            listener.update(event)


class Listener(abc.ABC):
    @abc.abstractmethod
    def update(self, event):
        raise NotImplementedError
