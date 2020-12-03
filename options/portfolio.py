import graphviz
import matplotlib.pyplot as plt
import numpy as np
from typing import List

PUT = +1
CALL = -1


def union(rng1, rng2):
    (l1, h1) = rng1
    (l2, h2) = rng2
    return min(l1, l2), max(h1, h2)


class Option:
    def __init__(self, kind: int, strike_price: int, price: int = 0):
        self.kind = kind
        self.strike_price = strike_price
        self.price = price

    def __repr__(self):
        if self.kind == PUT:
            return f'Put(strike = {self.strike_price})'
        elif self.kind == CALL:
            return f'Call(strike = {self.strike_price})'

    def range_of_interest(self):
        return (self.strike_price, self.strike_price)

    def value_at(self, stock_price: int):
        return np.maximum(self.kind * (self.strike_price - stock_price), 0)

    def profit_at(self, stock_price: int):
        return self.value_at(stock_price) - self.price

    def _repr_png_(self, fig_ax=None, fig_low=None, fig_high=None, linestyle='-', labels=None):
        fig, ax = plt.subplots() if fig_ax is None else fig_ax
        labels = [] if labels is None else labels

        low, high = self.range_of_interest()
        if fig_low is None:
            fig_low = low - max(10, 0.1*(high - low))
        if fig_high is None:
            fig_high = high + max(10, 0.1*(high - low))

        x = np.linspace(fig_low, fig_high, 100)
        y = self.value_at(x)
        labels.append(self.__repr__())

        ax.plot(x, y, linestyle)

        if fig_ax is None:
            fig.legend(labels)
            fig.close()
            return display(fig)


class Put(Option):
    def __init__(self, strike_price: int, price: int = 0):
        super().__init__(PUT, strike_price, price)


class Call(Option):
    def __init__(self, strike_price: int, price: int = 0):
        super().__init__(CALL, strike_price, price)


class Short(Option):
    def __init__(self, option: Option):
        self.option = option

    def value_at(self, stock_price: int):
        return -self.option.value_at(stock_price)

    def profit_at(self, stock_price: int):
        return self.value_at(stock_price) + self.option.price

    def range_of_interest(self):
        return self.option.range_of_interest()

    def __repr__(self):
        return f'Short({self.option})'

    @property
    def strike_price(self):
        return self.option.strike_price


class Portfolio(Option):
    def __init__(self, *options: List[Option]):
        self.options = options

    def __repr__(self):
        return 'Portfolio'

    def range_of_interest(self):
        rng = self.options[0].range_of_interest()
        for o in self.options:
            rng = union(rng, o.range_of_interest())
        return rng

    def value_at(self, stock_price):
        return sum(o.value_at(stock_price) for o in self.options)

    def _repr_png_(self, fig_ax=None, fig_low=None, fig_high=None, linestyle='-', labels=None):
        (fig, ax) = plt.subplots() if fig_ax is None else fig_ax
        labels = [] if labels is None else labels

        low, high = self.range_of_interest()
        if fig_low is None:
            fig_low = low - max(10, 0.1*(high - low))
        if fig_high is None:
            fig_high = high + max(10, 0.1*(high - low))

        for option in self.options:
            option._repr_png_((fig, ax), fig_low, fig_high,
                              linestyle='--', labels=labels)

        super()._repr_png_((fig, ax), fig_low, fig_high, linestyle, labels)

        if fig_ax is None:
            fig.legend(labels)
            fig.close()
            return display(fig)
