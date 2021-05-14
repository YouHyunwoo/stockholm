import pyupbit

from core.trader import Trader



class UpbitTrader(Trader):
    def authenticate(self, api_key):
        self.account = pyupbit.Upbit(**api_key['home'])

    def on_notify(self, subject, event, *args, **kwargs):
        if event == 'sell':
            ticker = args[0]
            coin_price = args[1]

            coin_balance = self.account.get_balance(ticker.code)

            if coin_price * coin_balance > 5000:
                self.account.sell_market_order(ticker.for_exchange, coin_balance * 0.9995)

        elif event == 'buy':
            ticker = args[0]
            price = args[1] if len(args) >= 2 else self.account.get_balance("KRW")

            if price > 5000:
                self.account.buy_market_order(ticker.for_exchange, price * 0.9995)
                subject.on_buy(ticker, price)
