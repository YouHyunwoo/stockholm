import time
import json

from core.investment import Investment
from core.logger import Logger
from core.ticker import Ticker

from strategy.volatility import VolatilityStrategy

from trader.upbit import UpbitTrader



class InvestorContext:
    def __init__(self):
        self.logger = None
        self.portfolio = None
        self.exchange = None
        self.api_key = None

        self.trader = None
        self.investments = None

    def initialize(self, portfolio):
        with open('data/portfolio/{}.json'.format(portfolio), 'r', encoding='utf8') as file:
            self.portfolio = json.load(file)
            assert self.portfolio['name'] == portfolio

        self.exchange = self.portfolio['exchange']

        with open('data/api/{}.json'.format(self.exchange), 'r', encoding='utf8') as file:
            self.api_key = json.load(file)

        if self.exchange == 'upbit':
            self.trader = UpbitTrader()
        else:
            raise Exception('not supported exchange')

        self.trader.authenticate(self.api_key)


class Investor:
    def __init__(self, portfolio):
        self.context = InvestorContext()
        self.context.initialize(portfolio)

    def invest(self):
        self.generate_investments()

        while True:
            for investment in self.context.investments:
                investment.update()

            time.sleep(1)

    def generate_investments(self):
        portfolio_name = self.context.portfolio['name']
        investment_items = self.context.portfolio['investment_items']
        trader = self.context.trader

        investments = []

        for investment_item in investment_items:
            ticker = Ticker(investment_item['code'], Ticker.UPBIT)
            strategy = VolatilityStrategy()
            logger = Logger(level=Logger.INFO, verbose=True, silent=False,
                            file='data/log/{}/{}.txt'.format(portfolio_name, ticker.code),
                            file_level=Logger.DEBUG)

            investment = Investment(ticker, trader, strategy, logger)

            investments.append(investment)

        self.context.investments = investments
