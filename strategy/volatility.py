import datetime
import pyupbit

from core.strategy import Strategy



class VolatilityContext:
	def __init__(self):
		self.K = 0.5

		self.market_start_time = None
		self.market_end_time = None
		self.range = None

		self.minimum_price = None
		self.target_price = None

		self.buying_price = None
		self.selling_price = None

	def reset(self):
		self.market_start_time = None
		self.market_end_time = None
		self.range = None

		self.minimum_price = None
		self.target_price = None

		self.buying_price = None
		self.selling_price = None


class VolatilityStrategy(Strategy):
	def __init__(self):
		super().__init__()

		self.context = VolatilityContext()

	def update(self, investment):
		if self.context.market_start_time is None:
			self.start_market(investment)
		elif investment.context.current_time >= self.context.market_end_time - datetime.timedelta(seconds=10):
			self.end_market(investment)
		else:
			self.update_market(investment)

		self.print_state(investment)

	def start_market(self, investment):
		ticker = investment.ticker

		df = pyupbit.get_ohlcv(ticker.for_exchange, interval="day", count=2)

		self.context.market_start_time = df.index[1]
		self.context.market_end_time = self.context.market_start_time + datetime.timedelta(days=1)

		self.context.range = abs(df.iloc[0]['close'] - df.iloc[0]['open'])

		self.context.minimum_price = investment.context.current_price

	def end_market(self, investment):
		self.sell(investment)

		self.context.reset()

	def sell(self, investment):
		ticker = investment.ticker
		coin_price = investment.context.current_price

		self.notify('sell', ticker, coin_price)

	def update_market(self, investment):
		current_price = investment.context.current_price
		minimum_price = min(current_price, self.context.minimum_price)

		target_price = minimum_price + self.context.range * self.context.K

		if target_price < current_price:
			self.buy(investment)

		self.context.minimum_price = minimum_price
		self.context.target_price = target_price

	def buy(self, investment):
		ticker = investment.ticker

		self.notify('buy', ticker)

	def print_state(self, investment):
		logger = investment.logger

		if logger is not None:
			if self.context.market_start_time is not None:
				logger.info('{:>30s}: {}'.format('market start time', self.context.market_start_time))
				logger.info('{:>30s}: {}'.format('market   end time', self.context.market_end_time))
				logger.info('{:>30s}: {}'.format('K', self.context.K))
				logger.info('{:>30s}: {}'.format('previous range', self.context.range))
				logger.info('{:>30s}: {}'.format('minimum price', self.context.minimum_price))
				logger.info('{:>30s}: {}'.format('target price', self.context.target_price))
				logger.info('[ BUY] | {} | {}'.format(investment.ticker.code, self.context.buying_price))
				logger.info('[SELL] | {} | {}'.format(investment.ticker.code, self.context.selling_price))

	def on_buy(self, ticker, price):
		self.context.buying_price = price

	def on_sell(self, ticker, price):
		self.context.selling_price = price
