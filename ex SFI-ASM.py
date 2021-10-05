import numpy as np
import pandas as pd


class Investor:
    """
    Agente investidor do modelo Santa Fe Institute - Artificial Stock Market.
    Referência capítulo 6 de "Agent-Based Modeling The Santa Fe Institute Artificial Stock Market Model Revisited"
    """

    def __init__(self, rules):
        """
        :param rules: lista de 100 objetos 'Rule', regras de decisão iniciais
        """
        self.stock_qty = 1
        self._risk_aversion_coef = 0.5
        self.tranding_rules = rules

    def stock_demand(self, current_price, expected_price, stock_variance, risk_free):
        opt_qty = (expected_price - current_price * (1 + risk_free)) / (self._risk_aversion_coef * stock_variance)
        return opt_qty - self.stock_qty


class Rule:
    """
    Regra de decisão baseada na estrutura de informações sobre o mercado
    """

    def __init__(self):
        self._alpha = 0
        self._beta = 0

    def forecast(self, p_d):
        return self._alpha * p_d + self._beta


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
    Conjunto de dados que serão avaliados. Seguindo nossa referência, teremos 64 elementos de informação de mercado.
    """

    def __init__(self, initial_price_df=None):
        self.dividend_mean = 10
        self.revision_speed = 0.5
        self.dividend_error_var = 0.1
        self.risk_free = 0.05
        self.rule_set = []
        self.current_state = [0 for i in range(0, 64)]

        if initial_price_df is not None:
            self.price_history = pd.DataFrame(data=None, columns=['step', 'price', 'dividend', 'variation', 'volume'])
        else:
            self.price_history = pd.DataFrame(data=initial_price_df, columns=['step', 'price', 'dividend',
                                                                              'variation', 'volume'])
        dividend_ratio_rule = [0.6, 0.8, 0.9, 1, 1.1, 1.12, 1.4]
        price_ratio_rule = [0.25, 0.5, 0.75, .875, 1, 1.125, 1.25]
        price_interest_ratio_rule = [0.25, 0.5, 0.75, .875, .95, 1, 1.125]

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
        # preco


    def update_info_state(self):
        for n, f in enumerate(self.rule_set):
            if n <= 5:
                self.current_state[n] = f(
                    self.price_history.dividend.tail(1).mean() / self.price_history.dividend.mean())
            elif n <= 14:
                self.current_state[n] = f(self.price_history.price.tail(1).mean() / self.price_history.preco.mean())
            elif n <= 20:
                self.current_state[n] = f(
                    self.price_history.price.tail(1) * self.risk_free / self.price_history.dividend.tail(1))
            elif n <= 25:
                self.current_state[n] = f(self.price_history.price.iloc[-n + 20] - self.price_history.price.iloc[-n + 21])
            elif n <= 29:
                self.current_state[n] = f(
                    self.price_history.dividend.iloc[-n + 25] - self.price_history.dividend.iloc[-n + 26])
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
                pass
        self.current_state[30] = (self.price_history.price.iloc[-5:].mean() > self.price_history.price.iloc[-6:-1].mean())
        self.current_state[31] = (self.price_history.price.iloc[-10:].mean() > self.price_history.price.iloc[-11:-1].mean())
        self.current_state[32] = (self.price_history.price.iloc[-20:].mean() > self.price_history.price.iloc[-21:-1].mean())
        self.current_state[33] = (self.price_history.price.iloc[-100:].mean() > self.price_history.price.iloc[-101:-1].mean())
        self.current_state[34] = (self.price_history.price.iloc[-500:].mean() > self.price_history.price.iloc[-501:-1].mean())
        self.current_state[35] = (self.price_history.dividend.iloc[-5:].mean() > self.price_history.price.iloc[-6:-1].mean())
        self.current_state[36] = (self.price_history.dividend.iloc[-10:].mean() > self.price_history.dividend.iloc[-11:-1].mean())
        self.current_state[37] = (self.price_history.dividend.iloc[-100:].mean() > self.price_history.dividend.iloc[-101:-1].mean())
        self.current_state[38] = (self.price_history.dividend.iloc[-500:].mean() > self.price_history.dividend.iloc[-501:-1].mean())
        self.current_state[39] = (self.price_history.price.iloc[-1:] > self.price_history.price.iloc[-5:].mean())
        self.current_state[40] = (
                    self.price_history.price.iloc[-1:] > self.price_history.price.iloc[-10:].mean())
        self.current_state[41] = (
                    self.price_history.price.iloc[-1:] > self.price_history.price.iloc[-20:].mean())
        self.current_state[42] = (
                    self.price_history.price.iloc[-1:] > self.price_history.price.iloc[-100:].mean())
        self.current_state[43] = (
                    self.price_history.price.iloc[-1:] > self.price_history.price.iloc[-500:].mean())
        self.current_state[44] = (
                self.price_history.dividend.iloc[-1:] > self.price_history.dividend.iloc[-5:].mean())
        self.current_state[45] = (
                self.price_history.dividend.iloc[-1:] > self.price_history.dividend.iloc[-10:].mean())
        self.current_state[46] = (
                self.price_history.dividend.iloc[-1:] > self.price_history.dividend.iloc[-100:].mean())
        self.current_state[47] = (
                self.price_history.dividend.iloc[-1:] > self.price_history.dividend.iloc[-500:].mean())
        self.current_state[48] = (
                self.price_history.dividend.iloc[-5:].mean() > self.price_history.dividend.iloc[-10:].mean())
        self.current_state[49] = (
                self.price_history.dividend.iloc[-5:].mean() > self.price_history.dividend.iloc[-100:].mean())
        self.current_state[50] = (
                self.price_history.dividend.iloc[-5:].mean() > self.price_history.dividend.iloc[-500:].mean())
        self.current_state[51] = (
                self.price_history.dividend.iloc[-10:].mean() > self.price_history.dividend.iloc[-100:].mean())
        self.current_state[52] = (
                self.price_history.dividend.iloc[-10:].mean() > self.price_history.dividend.iloc[-100:].mean())
        self.current_state[53] = (
                self.price_history.dividend.iloc[-10:].mean() > self.price_history.dividend.iloc[-10:].mean())
        self.current_state[54] = (
                self.price_history.price.iloc[-5:].mean() > self.price_history.price.iloc[-10:].mean())
        self.current_state[55] = (
                self.price_history.price.iloc[-5:].mean() > self.price_history.price.iloc[-20:].mean())
        self.current_state[56] = (
                self.price_history.price.iloc[-5:].mean() > self.price_history.price.iloc[-100:].mean())
        self.current_state[57] = (
                self.price_history.price.iloc[-5:].mean() > self.price_history.price.iloc[-500:].mean())
        self.current_state[58] = (
                self.price_history.price.iloc[-10:].mean() > self.price_history.price.iloc[-20:].mean())
        self.current_state[59] = (
                self.price_history.price.iloc[-10:].mean() > self.price_history.price.iloc[-100:].mean())
        self.current_state[60] = (
                self.price_history.price.iloc[-10:].mean() > self.price_history.price.iloc[-500:].mean())
        self.current_state[61] = (
                self.price_history.price.iloc[-20:].mean() > self.price_history.price.iloc[-100:].mean())
        self.current_state[62] = (
                self.price_history.price.iloc[-20:].mean() > self.price_history.price.iloc[-500:].mean())
        self.current_state[63] = (
                self.price_history.price.iloc[-100:].mean() > self.price_history.price.iloc[-500:].mean())

    def dividend_selector(self):
        pass