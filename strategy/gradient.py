import numpy as np

from core.strategy import Strategy



class GradientContext:
    def __init__(self):
        self.gradients = None

        self.is_bought = False
        self.bought_price = None

        self.decision = None

        self.rate_of_return = 1
        self.rate_of_return_with_premium = 1


class GradientStrategy(Strategy):
    def __init__(self):
        super().__init__()

        self.context = GradientContext()

    def update(self, investment):
        if len(investment.context.prices) >= 3:
            prices = investment.context.prices[-3:]

            self.context.gradients = np.diff(prices)

            self.print_gradients()

            prev_grad = self.context.gradients[-2]
            curr_grad = self.context.gradients[-1]

            self.context.decision = None

            if prev_grad >= 0 > curr_grad:
                if self.context.is_bought:
                    ticker = investment.ticker
                    message = (investment.context.current_price, )

                    self.notify('sell', ticker, message)

                    self.calculate_rate_of_return(investment.context.current_price)

                    self.context.is_bought = False
                    self.context.bought_price = None

                    self.context.decision = 'sell'

            elif curr_grad > 0 >= prev_grad:
                if not self.context.is_bought:
                    ticker = investment.ticker
                    message = (investment.context.current_price, )

                    self.notify('buy', ticker, message)

                    self.context.is_bought = True
                    self.context.bought_price = investment.context.current_price

                    self.context.decision = 'buy'

            self.print_decision(investment.context.current_price)
            self.print_rate_of_return()

    def print_gradients(self):
        prev_grad = self.context.gradients[-2]
        curr_grad = self.context.gradients[-1]

        print('  [Gradient] {:7.2f} -> {:7.2f}'.format(prev_grad, curr_grad))

    def calculate_rate_of_return(self, current_price):
        bought_price = self.context.bought_price

        rate_of_return = current_price / bought_price
        rate_of_return_with_premium = rate_of_return * 0.9995 / 1.0005

        self.context.rate_of_return *= rate_of_return
        self.context.rate_of_return_with_premium *= rate_of_return_with_premium

    def print_decision(self, current_price):
        sell_text = 'SELL' if self.context.decision == 'sell' else 'Sell'
        buy_text = 'BUY' if self.context.decision == 'buy' else 'Buy'

        print('  [{}/{}] {:18.2f}'.format(sell_text, buy_text, current_price))

    def print_rate_of_return(self):
        print('  [ROR ] {:.3f}'.format(self.context.rate_of_return))
        print('  [RORP] {:.3f}'.format(self.context.rate_of_return_with_premium))

    def on_buy(self, ticker, price):
        pass

    def on_sell(self, ticker, price):
        pass
