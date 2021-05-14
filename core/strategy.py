from util.pattern.observer import Subject



class Strategy(Subject):
    def update(self, investment):
        raise NotImplementedError

    def on_buy(self, ticker, price):
        raise NotImplementedError

    def on_sell(self, ticker, price):
        raise NotImplementedError
