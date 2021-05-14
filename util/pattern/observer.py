class Subject:
    def __init__(self):
        self.listeners = {}

    def add_event_listener(self, event, listener):
        if event not in self.listeners:
            self.listeners[event] = []

        self.listeners[event].append(listener)

    def remove_event_listener(self, event, listener):
        if event in self.listeners:
            self.listeners[event].remove(listener)

            if len(self.listeners[event]) <= 0:
                del self.listeners[event]

    def notify(self, event, *args, **kwargs):
        for listener in self.listeners[event]:
            listener.on_notify(self, event, *args, **kwargs)


class Observer:
    def on_notify(self, subject, event, *args, **kwargs):
        raise NotImplementedError
