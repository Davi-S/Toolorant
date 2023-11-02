import abc
import threading


class Listener(abc.ABC):
    @abc.abstractmethod
    def on_event(self, event):
        raise NotImplementedError


class Publisher:
    def __init__(self):
        self._listeners: set[Listener] = set()

    def add_listener(self, listener):
        self._listeners.add(listener)

    def remove_listener(self, listener):
        self._listeners.discard(listener)

    def _notify_listeners(self, listener: Listener, event):
        listener.on_event(event)

    def notify_listeners(self, event):
        # Notify listener on separated thread so the all listeners will be notified quickly even if one listener takes too long to return.
        for listener in self._listeners:
            threading.Thread(
                target=self._notify_listeners,
                name=f'PublisherNotifyListener{listener.__class__.__name__.title()}',
                args=(listener, event),
                daemon=True
            ).start()