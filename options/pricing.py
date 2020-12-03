import graphviz
import matplotlib.pyplot as plt
import numpy as np
from typing import List


def node_id(stock_price, period):
    return f'{period}_{stock_price}'


PUT = +1
CALL = -1


def current_value(stock_price, strike_price, option_type):
    return max(option_type * (strike_price - stock_price), 0)


def binomial_pricing(stock_price, strike_price, option_type, risk_free_rate, up, down, periods=1):
    dot = graphviz.Digraph()
    dot.graph_attr['rankdir'] = 'LR'
    _binomial_pricing(stock_price, strike_price, option_type,
                      risk_free_rate, up, down, {}, dot, periods=periods, current_period=0)
    return dot


def _binomial_pricing(stock_price, strike_price, option_type, risk_free_rate, up, down, memo=None, dot=None, periods=1, current_period=0):
    if current_period == periods:
        value = current_value(stock_price, strike_price, option_type)
        dot.node(node_id(stock_price, current_period),
                 f'STOCK = {stock_price:.4g}\n––––––––––––\nvalue = {value:.4g}')
        return value

    if (current_period, stock_price) in memo:
        return memo[(current_period, stock_price)]

    up_price = stock_price * up
    up_value = _binomial_pricing(up_price, strike_price, option_type,
                                 risk_free_rate, up, down, memo, dot, periods, current_period + 1)

    down_price = stock_price * down
    down_value = _binomial_pricing(down_price, strike_price, option_type,
                                   risk_free_rate, up, down, memo, dot, periods, current_period + 1)

    # We want up_price * S + B(1 + rf) = up_value
    # and down_price * S + B(r + rf) = down_value
    # => (up_price - down_price)S = up_value - down_value
    # => S = (up_value - down_value) / (up_price - down_price)
    S = (up_value - down_value) / (up_price - down_price)
    B = (up_value - up_price * S) / (1 + risk_free_rate)
    value = stock_price * S + B
    memo[(current_period, stock_price)] = value

    dot.node(node_id(stock_price, current_period),
             f'STOCK = {stock_price}\n––––––––––––\nvalue = {value:.4g}\nS = {S:.4g}\nB = {B:.4g}')
    dot.edge(node_id(stock_price, current_period),
             node_id(up_price, current_period + 1))
    dot.edge(node_id(stock_price, current_period),
             node_id(down_price, current_period + 1))

    return value


def _risk_neutral_probabilities(stock_price, strike_price, option_type, risk_free_rate, up, down, memo, dot, periods=1, current_period=0):
    if current_period == periods:
        value = current_value(stock_price, strike_price, option_type)
        dot.node(node_id(stock_price, current_period),
                 f'STOCK = {stock_price:.4g}\n––––––––––––\nvalue = {value:.4g}')
        return value

    if (current_period, stock_price) in memo:
        return memo[(current_period, stock_price)]

    up_price = stock_price * up
    up_value = _risk_neutral_probabilities(
        up_price, strike_price, option_type, risk_free_rate, up, down, memo, dot, periods, current_period + 1)

    down_price = stock_price * down
    down_value = _risk_neutral_probabilities(
        down_price, strike_price, option_type, risk_free_rate, up, down, memo, dot, periods, current_period + 1)

    # stock today = (p up_price + (1 - p) down_price) / (1 + r_f)
    # (1 + rf) today = p up + down - p down
    # p (up - down) = (1 + rf) today - down
    # p = [(1 + rf) today - down] / (up - down)
    p = ((1 + risk_free_rate) * stock_price -
         down_price) / (up_price - down_price)
    value = (p * up_value + (1 - p) * down_value) / (1 + risk_free_rate)
    memo[(current_period, stock_price)] = value

    dot.node(node_id(stock_price, current_period),
             f'STOCK = {stock_price}\n––––––––––––\nvalue = {value:.4g}\np = {p:.4g}')
    dot.edge(node_id(stock_price, current_period),
             node_id(up_price, current_period + 1), 'p')
    dot.edge(node_id(stock_price, current_period), node_id(
        down_price, current_period + 1), '1 - p')

    return value


def risk_neutral_probabilities(stock_price, strike_price, option_type, risk_free_rate, up, down, periods=1):
    dot = graphviz.Digraph()
    dot.graph_attr['rankdir'] = 'LR'
    _risk_neutral_probabilities(stock_price, strike_price, option_type,
                                risk_free_rate, up, down, {}, dot, periods=periods, current_period=0)
    return dot
