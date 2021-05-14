from util.pattern.observer import Observer



class Trader(Observer):
    def __init__(self):
        self.account = None

    def authenticate(self, api_key):
        raise NotImplementedError

    def on_notify(self, subject, event, *args, **kwargs):
        raise NotImplementedError


class NullTrader(Trader):
    def __init__(self):
        super().__init__()

    def authenticate(self, api_key):
        pass

    def on_notify(self, subject, event, *args, **kwargs):
        pass
