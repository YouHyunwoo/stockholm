class Ticker:
    UPBIT = 0

    def __init__(self, ticker, exchange):
        self.code = ticker

        if exchange == self.UPBIT:
            self.for_exchange = 'KRW-' + ticker
        else:
            self.for_exchange = ticker
