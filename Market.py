import datetime
import random
import csv
from decimal import Decimal
from statistics import mean

import numpy as np
import pandas as pd


def ratio_greater_than(k):
    def f(x, y):
        return (x / y) > k

    return f


def xyz_ratio_greater_than(k):
    def f(x, y, z):
        return x * y / z > k

    return f


class MarketInfo:
    """
    Classe que implementa as informações de mercado em geral, incluindo as séries de preço.
    Seguindo nossa referência, teremos 64 elementos de informação de mercado.
    """

    def __init__(self, dividend_mean, filepath="price.csv", initial_price=80):
        self.dividend_mean = dividend_mean
        self.revision_speed = 0.95
        self.dividend_error_var = 0.1
        self.risk_free = Decimal(0.05)
        self.rule_set = []
        self.current_state = [0 for i in range(0, 64)]
        self.price_history_path = filepath
        self.price_history = []
        self.dividend_history = []
        dividend_ratio_rule = [0.6, 0.8, 0.9, 1, 1.1, 1.12, 1.4]
        price_ratio_rule = [0.25, 0.5, 0.75, .875, 1, 1.125, 1.25]
        price_interest_ratio_rule = [0.25, 0.5, 0.75, .875, .95, 1, 1.125]
        """
        # Cria as regras de 0 a 5 (fundamental conditions) primeiras regras - razao entre dividendos e dividendo medio
        for i in range(0, 7):
            self.rule_set.append(ratio_greater_than(dividend_ratio_rule[i]))

        # Cria as regras 6 a 14 (technical conditions) - razao entre preco e preco medio

        for i in range(0, 7):
            self.rule_set.append(ratio_greater_than(price_ratio_rule[i]))

        # Cria as regras 15 a 20 (fundamental conditions) - razao entre precos*juros e dividendo

        for i in range(0, 7):
            self.rule_set.append(xyz_ratio_greater_than(price_interest_ratio_rule[i]))

        # Cria as regras 21 a 25 (technical conditions) - sentido dos preços

        for i in range(0, 5):
            self.rule_set.append(lambda x: x > 0)

        # Cria as regras 26 a 29 (fundamental conditions) - sentido dos dividendos

        for i in range(0, 4):
            self.rule_set.append(lambda x: x > 0)

        # Cria as regras 30 a 34 (fundamental conditions) - sentido da média móvel dos preços
        # Cria as regras 35 a 38 (fundamental conditions) - sentido da média móvel dos dividendos
        # Cria as regras 39 a 43 (technical conditions) - verifica se preco é maior que sua média móvel
        # Cria as regras 44 a 47 (fundamental conditions) - verifica se dividendo é maior que sua média móvel
        # Cria as regras 48 a 53 (fundamental conditions) - verifica media movel dividendo é maior que sua média móvel
        # Cria as regras 54 a 63 (technical conditions) - verifica media movel preco é maior que outras média móveis
        # preco"""

    def update_info_state(self, step):
        """for n, f in enumerate(self.rule_set):
            if n <= 5:
                pass
                # self.current_state[n] = f(self.price_history.dividend.tail(1).mean(), self.price_history.dividend.mean())
            elif n <= 14:
                pass
                # self.current_state[n] = f(self.price_history.price.tail(1).mean(), self.price_history.preco.mean())
            elif n <= 20:
                pass
                # self.current_state[n] = f(
                #    self.price_history.price.tail(1), self.risk_free, self.price_history.dividend.tail(1))
            elif n <= 25:
                pass
                # self.current_state[n] = f(
                #    self.price_history.price.iloc[-n + 20] - self.price_history.price.iloc[-n + 21])
            elif n <= 29:
                pass
                # self.current_state[n] = f(
                #    self.price_history.dividend.iloc[-n + 25] - self.price_history.dividend.iloc[-n + 26])
            elif n <= 34:
                pass
            elif n <= 38:
                pass
            elif n <= 43:
                pass
            elif n <= 47:
                pass
            elif n <= 53:
                pass
            else:
                pass  # [0.25, 0.5, 0.75, .875, .95, 1, 1.125]"""
        self.current_state[0] = bool(Decimal(self.dividend_history[-1]) / Decimal(mean(self.dividend_history)) > 0.6)
        self.current_state[1] = bool(
            Decimal(self.dividend_history[-1]) / Decimal(mean(self.dividend_history)) > 0.8)
        self.current_state[2] = bool(
            Decimal(self.dividend_history[-1]) / Decimal(mean(self.dividend_history)) > 0.9)
        self.current_state[3] = bool(
            Decimal(self.dividend_history[-1]) / Decimal(mean(self.dividend_history)) > 1.1)
        self.current_state[4] = bool(
            Decimal(self.dividend_history[-1]) / Decimal(mean(self.dividend_history)) > 1.12)
        self.current_state[5] = bool(
            Decimal(self.dividend_history[-1]) / Decimal(mean(self.dividend_history)) > 1.4)
        self.current_state[6] = bool(
            Decimal(self.price_history[-1]) / Decimal(mean(self.price_history)) > 0.25)
        self.current_state[7] = bool(
            Decimal(self.price_history[-1]) / Decimal(mean(self.price_history)) > 0.5)
        self.current_state[8] = bool(
            Decimal(self.price_history[-1]) / Decimal(mean(self.price_history)) > 0.75)
        self.current_state[9] = bool(
            Decimal(self.price_history[-1]) / Decimal(mean(self.price_history)) > 0.875)
        self.current_state[10] = bool(
            Decimal(self.price_history[-1]) / Decimal(mean(self.price_history)) > 1)
        self.current_state[11] = bool(
            Decimal(self.price_history[-1]) / Decimal(mean(self.price_history)) > 1.125)
        self.current_state[12] = bool(
            Decimal(self.price_history[-1]) / Decimal(mean(self.price_history)) > 1.25)
        self.current_state[13] = bool(
            Decimal(self.price_history[-1]) * self.risk_free / Decimal(mean(self.dividend_history)) > 0.25)
        self.current_state[14] = bool(
            Decimal(self.price_history[-1]) * self.risk_free / Decimal(mean(self.dividend_history)) > 0.5)
        self.current_state[15] = bool(
            Decimal(self.price_history[-1]) * self.risk_free / Decimal(mean(self.dividend_history)) > 0.75)
        self.current_state[16] = bool(
            Decimal(self.price_history[-1]) * self.risk_free / Decimal(mean(self.dividend_history)) > 0.875)
        self.current_state[17] = bool(
            Decimal(self.price_history[-1]) * self.risk_free / Decimal(mean(self.dividend_history)) > 0.95)
        self.current_state[18] = bool(
            Decimal(self.price_history[-1]) * self.risk_free / Decimal(mean(self.dividend_history)) > 1)
        self.current_state[19] = bool(
            Decimal(self.price_history[-1]) * self.risk_free / Decimal(mean(self.dividend_history)) > 1.125)
        if step > 10:
            self.current_state[20] = bool(self.price_history[-1] - self.price_history[-2] > 0)
            self.current_state[21] = bool(self.price_history[-2] - self.price_history[-3] > 0)
            self.current_state[22] = bool(self.price_history[-3] - self.price_history[-4] > 0)
            self.current_state[23] = bool(self.price_history[-4] - self.price_history[-5] > 0)
            self.current_state[24] = bool(self.price_history[-5] - self.price_history[-6] > 0)
            self.current_state[25] = bool(self.price_history[-6] - self.price_history[-7] > 0)
            self.current_state[26] = bool(self.dividend_history[-1] - self.dividend_history[-2] > 0)
            self.current_state[27] = bool(self.dividend_history[-2] - self.dividend_history[-3] > 0)
            self.current_state[28] = bool(self.dividend_history[-3] - self.dividend_history[-4] > 0)
            self.current_state[29] = bool(self.dividend_history[-4] - self.dividend_history[-5] > 0)
        self.current_state[30] = bool(mean(self.price_history[-5:]) > mean(self.price_history[-6:-1]))
        self.current_state[31] = bool(mean(self.price_history[-10:]) > mean(self.price_history[-11:-1]))
        self.current_state[32] = bool(mean(self.price_history[-20:]) > mean(self.price_history[-21:-1]))
        self.current_state[33] = bool(mean(self.price_history[-100:]) > mean(self.price_history[-101:-1]))
        self.current_state[34] = bool(mean(self.price_history[-500:]) > mean(self.price_history[-501:-1]))
        self.current_state[35] = bool(mean(self.dividend_history[-5:]) > mean(self.dividend_history[-6:-1]))
        self.current_state[36] = bool(mean(self.dividend_history[-10:]) > mean(self.dividend_history[-11:-1]))
        self.current_state[37] = bool(mean(self.dividend_history[-100:]) > mean(self.dividend_history[-101:-1]))
        self.current_state[38] = bool(mean(self.dividend_history[-500:]) > mean(self.dividend_history[-501:-1]))
        self.current_state[39] = bool(self.price_history[-1] > mean(self.price_history[-5:]))
        self.current_state[40] = bool(self.price_history[-1] > mean(self.price_history[-10:]))
        self.current_state[41] = bool(self.price_history[-1] > mean(self.price_history[-20:]))
        self.current_state[42] = bool(self.price_history[-1] > mean(self.price_history[-100:]))
        self.current_state[43] = bool(self.price_history[-1] > mean(self.price_history[-500:]))
        self.current_state[44] = bool(self.dividend_history[-1] > mean(self.dividend_history[-5:]))
        self.current_state[45] = bool(self.dividend_history[-1] > mean(self.dividend_history[-10:]))
        self.current_state[46] = bool(self.dividend_history[-1] > mean(self.dividend_history[-100:]))
        self.current_state[47] = bool(self.dividend_history[-1] > mean(self.dividend_history[-500:]))
        self.current_state[48] = bool(mean(self.dividend_history[-5:]) > mean(self.dividend_history[-10:]))
        self.current_state[49] = bool(mean(self.dividend_history[-5:]) > mean(self.dividend_history[-100:]))
        self.current_state[50] = bool(mean(self.dividend_history[-5:]) > mean(self.dividend_history[-500:]))
        self.current_state[51] = bool(mean(self.dividend_history[-10:]) > mean(self.dividend_history[-100:]))
        self.current_state[52] = bool(mean(self.dividend_history[-10:]) > mean(self.dividend_history[-500:]))
        self.current_state[53] = bool(mean(self.dividend_history[-100:]) > mean(self.dividend_history[-500:]))
        self.current_state[54] = bool(mean(self.price_history[-5:]) > mean(self.price_history[-10:]))
        self.current_state[55] = bool(mean(self.price_history[-5:]) > mean(self.price_history[-20:]))
        self.current_state[56] = bool(mean(self.price_history[-5:]) > mean(self.price_history[-100:]))
        self.current_state[57] = bool(mean(self.price_history[-5:]) > mean(self.price_history[-500:]))
        self.current_state[58] = bool(mean(self.price_history[-10:]) > mean(self.price_history[-20:]))
        self.current_state[59] = bool(mean(self.price_history[-10:]) > mean(self.price_history[-100:]))
        self.current_state[60] = bool(mean(self.price_history[-10:]) > mean(self.price_history[-500:]))
        self.current_state[61] = bool(mean(self.price_history[-20:]) > mean(self.price_history[-100:]))
        self.current_state[62] = bool(mean(self.price_history[-20:]) > mean(self.price_history[-500:]))
        self.current_state[63] = bool(mean(self.price_history[-100:]) > mean(self.price_history[-500:]))

    @staticmethod
    def write_step(step, price, dividend, variation, volume, is_rationed, pct_bit, excess_demand, file_obj,
                   header=False):
        df = dict(step=step, price=Decimal(price), dividend=Decimal(dividend), variation=variation, volume=volume,
                  is_rationed=is_rationed, pct_zero_bit=pct_bit, excess_demand=excess_demand)
        writer = csv.writer(file_obj,delimiter=';')
        if header:
            writer.writerow(
                ['step', 'price', 'dividend', 'variation', 'volume', 'is_rationed', 'pct_bit', 'excess_demand'])
        writer.writerow(list(df.values()))

    def update_history(self, price, dividend):
        self.price_history.append(price)
        self.dividend_history.append(dividend)

    def unburden_history(self):
        if len(self.price_history) >= 505:
            del self.price_history[0]
            del self.dividend_history[0]


class Stock:

    def __init__(self, initial_price, initial_dividend, dividend_mean, revision_speed, dividend_error_var=0.075,
                 reproduce=False):
        self.dividend_mean = Decimal(dividend_mean)
        self.current_price = Decimal(initial_price)
        self.current_dividend = Decimal(initial_dividend)
        self.revision_speed = Decimal(revision_speed)
        self.dividend_error_var = float(dividend_error_var)
        self.reproduce = bool(reproduce)

    def update_dividend(self):
        if self.reproduce:
            random.seed(0)
        error = Decimal(random.gauss(0, self.dividend_error_var))
        new_dividend = self.dividend_mean + self.revision_speed * (self.current_dividend - self.dividend_mean) + error
        self.current_dividend = Decimal(new_dividend)

    def update_price(self, price):
        self.current_price = price

