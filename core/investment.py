import datetime
import pyupbit



class InvestmentContext:
    def __init__(self, price_count):
        self.current_time = None
        self.current_price = None

        self.start_time = None
        self.prices = []
        self.price_count = price_count


class Investment:
    def __init__(self, ticker, trader, strategy, logger=None):
        self.ticker = ticker

        self.trader = trader
        self.strategy = strategy
        self.logger = logger

        self.context = InvestmentContext(price_count=30)

        self.strategy.add_event_listener('buy', self.trader)
        self.strategy.add_event_listener('sell', self.trader)

    def update(self):
        self.get_current_time()
        self.get_current_price()

        self.log()

        self.calculate_strategy()

    def get_current_time(self):
        curr_time = datetime.datetime.now()

        if self.context.start_time is None:
            self.context.start_time = curr_time

        self.context.current_time = curr_time

    def get_current_price(self):
        curr_price = pyupbit.get_current_price(self.ticker.for_exchange)

        self.context.current_price = curr_price

        self.context.prices.append(curr_price)

        if len(self.context.prices) > self.context.price_count:
            self.context.prices = self.context.prices[1:]

    def log(self):
        message = '{:>4s} | {} | {}'.format(
            self.ticker.code,
            self.context.current_time,
            self.context.current_price
        )

        self.logger.info(message)

    def calculate_strategy(self):
        self.strategy.update(self)
