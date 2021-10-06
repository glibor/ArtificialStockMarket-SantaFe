import random
import statistics
import math


class Investor:
    """
    Agente investidor do modelo Santa Fe Institute - Artificial Stock Market.
    Referência capítulo 6 de "Agent-Based Modeling The Santa Fe Institute Artificial Stock Market Model Revisited"
    """

    def __init__(self, rules, stock_qty=1, cash=20000, risk_free=0):
        """
        :param rules: lista de 100 objetos 'Rule', regras de decisão iniciais
        """
        self.stock_qty = stock_qty
        self.risk_aversion_coef = 0.5
        self.trading_rules = rules
        self.median_accuracy = 2
        self.cash = cash
        self.risk_free = risk_free

    def stock_demand(self, current_price):
        opt_qty = (self.trading_rules[0].forecast(current_price) - current_price * (1 + self.risk_free)) / (
                self.risk_aversion_coef * self.trading_rules[0].accuracy)
        return opt_qty - self.stock_qty

    def expected_price(self, price):
        self.trading_rules[0].forecast(price)

    def demand_derivative(self):
        """
        Retorna a derivada da demanda para verificar se o mercado está em equilíbrio

        :param current_price:
        :param risk_free:
        :return:
        """
        demand_derivative = (self.trading_rules[0].get_coefs()[0] - 1 - self.risk_free) / \
                            (self.risk_aversion_coef * self.trading_rules[0].accuracy)
        return demand_derivative

    def sort_rules_by_fitness(self):
        """
        Atualiza as regras de acordo com fitness
        Resultado self.trading_rules com regras da melhor para a pior
        """
        self.trading_rules = sorted(self.trading_rules, key=lambda rule: -rule.fitness)

    def update_median_accuracy(self):
        """
        Atualiza a mediana da precisão desse agente
        """
        accuracy = [i.accuracy for i in self.trading_rules]
        self.median_accuracy = statistics.median(accuracy)

    def GeneticAlgo(self, genetic_param):
        """
        Roda o algoritmo genético para este indivíduo. Deve ser rodado depois de sort_rules

        Resultado: Nova rule_set
        """
        index_list = [i for i in range(44, 64)]
        for _ in index_list:
            rand = random.uniform(0, 1)
            if rand < genetic_param:
                self.trading_rules[_].mutate_rule(accuracy=self.median_accuracy)
            else:
                rule1, rule2 = random.choice([self.trading_rules]), random.choice([self.trading_rules])
                self.trading_rules[_] = self.crossover(rule1, rule2)

    @staticmethod
    def crossover(rule1, rule2):
        """
        Geração "genética" de regras a partir de 2 outras regras

        :param rule1: Regra antiga
        :param rule2: regra antiga 2
        :return: Nova regra
        """
        nova_watchlist = []
        for i in range(64):
            if rule1.watch_list[i] == rule2.watch_list[i]:
                nova_watchlist[i] = rule1.watch_list[i]
            else:
                nova_watchlist[i] = random.choice([rule1.watch_list[i], rule2.watch_list[i]])
        rand = random.choice([0, 1, 2])
        if rand == 1:
            r_rand = random.choice([rule1, rule2])
            a, b = r_rand.get_coefs()
        elif rand == 2:
            a1, b1 = rule1.get_coefs()
            a2, b2 = rule2.get_coefs()
            a = random.choice(a1, a2)
            b = random.choice(b1, b2)
        else:
            a1, b1 = rule1.get_coefs()
            a2, b2 = rule2.get_coefs()
            a = (a1 / rule1.accuracy + a2 / rule2.accuracy) / (1 / rule1.accuracy + 1 / rule2.accuracy)
            b = (b1 / rule1.accuracy + b2 / rule2.accuracy) / (1 / rule1.accuracy + 1 / rule2.accuracy)
        nova_regra = Rule(nova_watchlist, a, b)
        nova_regra.accuracy = (rule1.accuracy + rule2.accuracy) / 2
        return nova_regra


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
        self.specifity = 64 - watch_list.count(2)

    def get_coefs(self):
        return self._alpha, self._beta

    def get_new_coeficients(self):
        a = random.uniform(0.7, 1.2)
        b = random.uniform(-10, 19)
        self._alpha = a
        self._beta = b

    def mutate_rule(self, reproduce=False, accuracy=2):
        self.accuracy = accuracy
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
        for i in self.watch_list:
            rand2 = random.uniform(0, 1)
            if rand2 <= 0.03:
                if self.watch_list[i] == 0:
                    rand3 = random.uniform(0, 1)
                    if rand3 <= 1 / 3:
                        self.watch_list[i] = 1
                    else:
                        self.watch_list[i] = 2
                elif self.watch_list[i] == 1:
                    rand3 = random.uniform(0, 1)
                    if rand3 <= 1 / 3:
                        self.watch_list[i] = 0
                    else:
                        self.watch_list[i] = 2
                else:
                    self.watch_list[i] = random.choice([0, 1, 2])

    def generalize_rule(self):
        """
        Método para generalizar regra após 4000 rodadas sem ser ativada
        :return:
        """
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
        fitness = 100 - (accuracy + bit_cost * self.specifity)
        self.accuracy = accuracy
        self.fitness = fitness


class Specialist:

    def __init__(self, max_trials, max_price, min_price, num_shares, min_excess, eta):
        self.max_trials = max_trials
        self.max_price = max_price
        self.min_price = min_price
        self.num_shares = num_shares
        self.min_excess = min_excess
        self.eta = eta

    def find_new_price(self, last_price, last_dividend, investors):
        """
        Método que tenta achar o preço que ajusta oferta e demanda. Deve ser chamado um número N de vezes

        :param last_dividend: último dividendo para ser usado na previsão dos preços
        :param investors: lista dos agente
        :param last_price: preço de período anterior
        :return: preço efetivo do período de agora
        """
        # TODO: Verificar o que fazer com normalized demands
        done = False
        trial_count = 0
        trialprice = last_price
        investor_demands = []
        num_agents = len(investors)
        slope_total = 0
        is_rationed = False

        # ---------- início do processo -----------------------------------------------------------------

        while trial_count <= self.max_trials and not done:
            for i in investors:
                investor_demands.append(investors[i].stock_demand(trialprice + last_dividend))
            if abs(sum(investor_demands)) <= self.min_excess:
                done = True
            if slope_total != 0:
                trialprice -= sum(investor_demands) / slope_total
            else:
                trialprice *= 1 + self.eta * sum(investor_demands)

            slope_total = sum([investors[i].demand_derivative() for i in range(num_agents)])
            if trialprice > self.max_price:
                trialprice = self.max_price
            if trialprice < self.min_price:
                trialprice = self.min_price

            trial_count += 1
            if trial_count < self.max_trials and done is False:
                investor_demands = []
        if done is False:
            is_rationed = True

        return trialprice, is_rationed

    # TODO: Implementar as vendas propriamente ditas
