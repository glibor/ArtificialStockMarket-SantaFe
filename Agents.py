import random


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

    def GeneticAlgo(self):
        pass

    def crossover_type1(self, rule1, rule2):
        pass

    def crossover_type2(self, rule1, rule2):
        pass


class Rule:
    """
    Regra de decisão baseada na estrutura de informações sobre o mercado
    """

    def __init__(self, watch_list, alpha=0, beta=0):
        """
        :param watch_list: lista de 64 posições com: 0,se esperar a posição ser 0, 1 se esperar 1 e 2 se for indiferente
        """
        self._alpha = alpha
        self._beta = beta
        self.watch_list = watch_list
        self.fitness = 0
        self.accuracy = 0
        self.specifity = 64-watch_list.count(2)

    def get_new_coeficients(self):
        a = random.uniform(0.7, 1.2)
        b = random.uniform(-10, 19)
        self._alpha = a
        self._beta = b

    def mutate_rule(self, reproduce=False):
        if not reproduce:
            random.seed(0)
        rand = random.uniform(0, 1)
        if rand <= 0.2:
            self.get_new_coeficients()
        elif rand <= 0.4:
            self._alpha = random.uniform(self._alpha * 0.95, self._alpha * 1.05)
            self._beta = random.uniform(self._beta * 0.95, self._beta * 1.05)
        else:
            pass

    def forecast(self, p_d):
        return self._alpha * p_d + self._beta

    def is_active(self, market_state):
        """
        verifica se a regra está ativa

        :param market_state: Binary 64 list representando as 64 informações
        :return: boolean
        """
        response = True
        for n, i in enumerate(market_state):
            if self.watch_list[n] == i:
                pass
            elif self.watch_list[n] != 2:
                response *= False
        return response

    def update_fitness_accuracy(self, pt, pt_1, dt, dt_1, teta, bit_cost):
        """
        Atualiza o valor dos atributos fitness e accuracy

        :param pt: preço realizado
        :param pt_1: preço anterior, usado na previsão
        :param dt: dividendo realizado
        :param dt_1: dividendo anterior, usado na previsão
        :param teta: velocidade da aprendizagem (parâmetro do modelo)
        :param bit_cost: parâmetro do custo de observar alguma informação
        """
        accuracy = (1 - (teta ^ -1)) * self.accuracy + (teta ^ -1) * (pt + dt - self.forecast(pt_1 + dt_1)) ** 2
        fitness = 100-(accuracy+bit_cost*self.specifity)
        self.accuracy = accuracy
        self.fitness = fitness


class Specialist:
    pass
