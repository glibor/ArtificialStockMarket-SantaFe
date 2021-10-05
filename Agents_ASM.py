

class Investor:
    """
    Agente investidor do modelo Santa Fe Institute - Artificial Stock Market.
    Referência capítulo 6 de "Agent-Based Modeling The Santa Fe Institute Artificial Stock Market Model Revisited"
    """

    def __init__(self, rules, stock_qty=1):
        """
        :param rules: lista de 100 objetos 'Rule', regras de decisão iniciais
        """
        self.stock_qty = stock_qty
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

class Specialist:
    pass
