"""Système d'événements découplé de Tkinter."""


class Event:
    """Un événement nommé avec des données associées."""

    def __init__(self, name, **data):
        self.name = name
        self.data = data


class EventBus:
    """Bus d'événements : permet d'émettre et d'écouter des événements."""

    def __init__(self):
        self._handlers = {}

    def on(self, name, handler):
        self._handlers.setdefault(name, []).append(handler)

    def off(self, name, handler):
        """Désabonne un handler d'un événement."""
        handlers = self._handlers.get(name)
        if handlers and handler in handlers:
            handlers.remove(handler)
            if not handlers:
                self._handlers.pop(name, None)

    def emit(self, name, **data):
        for handler in list(self._handlers.get(name, [])):
            handler(Event(name, **data))
