import random
import statistics
import math
from decimal import Decimal
from operator import attrgetter
import heapq

import pandas as pd


class Investor:
    """
    Agente investidor do modelo Santa Fe Institute - Artificial Stock Market.
    Referência capítulo 6 de "Agent-Based Modeling The Santa Fe Institute Artificial Stock Market Model Revisited"
    """

    def __init__(self, rules, stock_qty=1, cash=20000, risk_free=0.05):
        """
        :param rules: lista de 100 objetos 'Rule', regras de decisão iniciais
        """
        self.stock_qty = Decimal(stock_qty)
        self.risk_aversion_coef = Decimal(0.5)
        self.trading_rules = rules
        self.median_accuracy = Decimal(4)
        self.cash = Decimal(cash)
        self.risk_free = Decimal(risk_free)
        self.investor_history = pd.DataFrame(data=None, columns={'step', 'cash', 'stocks', 'wealth', 'bits_used',
                                                                 'alpha', 'beta', 'accuracy'})

    def stock_demand(self, current_price, market_state, dividend):
        rule = self.select_rule(market_state)
        if (self.risk_aversion_coef * Decimal(rule.accuracy)) != 0:
            opt_qty = (rule.forecast(Decimal(current_price) + Decimal(dividend)) - Decimal(current_price) * (
                    1 + self.risk_free)) / (
                              self.risk_aversion_coef * Decimal(rule.accuracy))
        else:
            opt_qty = 1
        if opt_qty * Decimal(current_price) > self.cash:
            opt_qty = self.cash / Decimal(current_price) + self.stock_qty
        if opt_qty <= -self.stock_qty:
            opt_qty = 0

        return opt_qty - self.stock_qty

    def effective_demand(self, current_price, market_state, dividend):
        qty = self.stock_demand(current_price, market_state, dividend)
        return qty - self.stock_qty

    def expected_price(self, price, market_state):
        self.select_rule(market_state).forecast(price)

    def demand_derivative(self, market_state):
        """
        Retorna a derivada da demanda para verificar se o mercado está em equilíbrio

        :param market_state: bits do mercado, lista de 64 elementos BOOL
        :return: derivada da demanda
        """
        rule = self.select_rule(market_state)
        a = rule.get_coefs()[0]
        demand_derivative = (a - 1 - self.risk_free) / (self.risk_aversion_coef * Decimal(rule.accuracy))
        return demand_derivative

    def sort_rules_by_fitness(self):
        """
        Atualiza as regras de acordo com fitness
        Resultado self.trading_rules com regras da melhor para a pior
        """
        self.trading_rules = sorted(self.trading_rules, key=lambda rule: rule.fitness)

    def select_rule(self, market_state):
        """
        Escolhe a melhor regra de decisão que esteja ativada

        :return: regra escolhida
        """
        done = False
        max_index = len(self.trading_rules)
        index = 0
        active_rules =[]
        while index < max_index and done is False:
            if self.trading_rules[index].is_active(market_state):
                active_rules.append(self.trading_rules[index])
                #rule = self.trading_rules[index]
                #done = True
            index += 1
        try:
            rule = max(active_rules, key=lambda x: x.accuracy)
            done = True
        except ValueError:
            pass
        if done is False:
            rule = Rule([2 for _ in range(64)])
            weigths = [Decimal(1 / r.accuracy) for r in self.trading_rules]
            a = sum([weigths[i] * Decimal(self.trading_rules[i]._alpha) for i in range(len(weigths))]) / Decimal(
                sum(weigths))
            b = sum([weigths[i] * Decimal(self.trading_rules[i]._beta) for i in range(len(weigths))]) / Decimal(
                sum(weigths))
            rule.set_coefs(a, b)

        return rule

    def update_median_accuracy(self):
        """
        Atualiza a mediana da precisão desse agente
        """
        accuracy = [i.accuracy for i in self.trading_rules]
        self.median_accuracy = statistics.median(accuracy)

    def update_portifolio(self, qnty, price,dividend):
        #self.cash += Decimal(dividend) * self.stock_qty
        self.stock_qty += Decimal(qnty)
        self.cash -= Decimal(qnty) * Decimal(price)

    def genetic_algo(self, genetic_param):
        """
        Roda o algoritmo genético para este indivíduo. Deve ser rodado depois de sort_rules

        Resultado: Nova rule_set
        """
        index_list = [i for i in range(44, 64)]
        #rule_list = heapq.nsmallest(20, self.trading_rules, key=lambda x: -x.accuracy)
        for i in index_list:
            rand = random.uniform(0, 1)
            if rand < genetic_param:
                self.trading_rules[i].mutate_rule(accuracy=self.median_accuracy)
            else:
                rule1, rule2 = random.choice(self.trading_rules), random.choice(self.trading_rules)
                self.trading_rules[i] = self.crossover(rule1, rule2)

    def write_to_df(self, step, cash, stocks, wealth, bits_used,alpha, beta, accuracy):
        df = dict(step=step, cash=cash, stocks=stocks, wealth=wealth, bits_used=bits_used,
                  alpha=alpha, beta=beta, accuracy=accuracy)
        # df = pd.DataFrame(df)
        self.investor_history = self.investor_history.append(df, ignore_index=True)

    @staticmethod
    def crossover(rule1, rule2):
        """
        Geração "genética" de regras a partir de 2 outras regras

        :param rule1: Regra antiga
        :param rule2: regra antiga 2
        :return: Nova regra
        """
        nova_watchlist = [2 for _ in range(64)]
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
            a = random.choice([a1, a2])
            b = random.choice([b1, b2])
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
        self._maxError = 10
        self.watch_list = watch_list
        self.specificity = 64 - watch_list.count(2)
        self.accuracy = 4
        self.bit_cost = 0.005
        self.unused_steps = 0
        #self.fitness = 100 - (self.accuracy[-1] + self.bit_cost * self.specificity)

    @property
    def fitness(self):
        return 100 - (Decimal(self.accuracy) + Decimal(self.bit_cost) * self.specificity)

    def get_coefs(self):
        return Decimal(self._alpha), Decimal(self._beta)

    def get_new_coeficients(self):
        a = random.uniform(0.7, 1.2)
        b = random.uniform(-10, 19)
        self._alpha = Decimal(a)
        self._beta = Decimal(b)

    def mutate_rule(self, reproduce=False,accuracy=4):
        self.accuracy = accuracy
        if not reproduce:
            random.seed(0)
        rand = random.uniform(0, 1)
        if rand <= 0.2:
            self.get_new_coeficients()
        elif rand <= 0.4:
            self._alpha = Decimal(random.uniform(self._alpha * 0.95, self._alpha * 1.05))
            self._beta = Decimal(random.uniform(self._beta * 0.95, self._beta * 1.05))
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
        return Decimal(self._alpha) * Decimal(p_d) + Decimal(self._beta)

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

    def update_fitness_accuracy(self, pt, pt_1, dt, dt_1, teta, bit_cost=0.005):
        """
        Atualiza o valor dos atributos fitness e accuracy

        :param pt: preço realizado
        :param pt_1: preço anterior, usado na previsão
        :param dt: dividendo realizado
        :param dt_1: dividendo anterior, usado na previsão
        :param teta: velocidade da aprendizagem (parâmetro do modelo)
        :param bit_cost: parâmetro do custo de observar alguma informação
        """
        error = (Decimal(pt) + Decimal(dt) - self.forecast(Decimal(pt_1) + Decimal(dt_1))) ** 2
        if error > 100:
            error = Decimal(100)
        accuracy = (1 - Decimal(teta ** -1)) * Decimal(self.accuracy) + Decimal(teta ** -1) * error
        # fitness = 100 - (Decimal(accuracy) + Decimal(bit_cost) * self.specificity)
        self.accuracy = accuracy

    def set_coefs(self, a, b):
        self._alpha = a
        self._beta = b


class Specialist:

    def __init__(self, max_trials, max_price, min_price, num_shares, min_excess, eta):
        self.max_trials = max_trials
        self.max_price = max_price
        self.min_price = min_price
        self.num_shares = num_shares
        self.min_excess = min_excess
        self.eta = Decimal(eta)

    def calculate_demands(self, last_price, last_dividend, investors, market_state, zero_excess=False):
        """
        Método que tenta achar o preço que ajusta oferta e demanda. Deve ser chamado um número N de vezes

        :param zero_excess:
        :param market_state:
        :param last_dividend: último dividendo para ser usado na previsão dos preços
        :param investors: lista dos agente
        :param last_price: preço de período anterior
        :return: demandas finais e BOOL de racionamento
        """

        done = False
        trial_count = 0
        trialprice = Decimal(last_price)
        investor_demands = []
        num_agents = len(investors)
        slope_total = 0
        is_rationed = False

        """def normalize_demands(demands, p_trial):
            for idx in range(num_agents):
                # restringe oferta à quantidade que o agente possui
                if demands[idx] < -investors[idx].stock_qty:
                    demands[idx] = -investors[idx].stock_qty
                # restringe demanda ao dinheiro que o agente possui
                elif demands[idx] * p_trial > investors[idx].cash:
                    demands[idx] = math.floor(investors[idx].cash / p_trial)

            normalization_numer = abs(sum([x for x in demands if x < 0]))
            normalization_denom = sum([x for x in demands if x > 0])
            for idx in range(len(demands)):
                if demands[idx] > 0:
                    demands[idx] = demands[idx] * normalization_numer / normalization_denom
            return demands
        """
        # ---------- início do processo -----------------------------------------------------------------

        while trial_count <= self.max_trials - 1 and not done:
            for i in investors:
                investor_demands.append(i.stock_demand(trialprice, market_state, last_dividend))
            # investor_demands = [i.stock_demand(trialprice + last_dividend)) for i in investors]
            if abs(sum(investor_demands)) <= self.min_excess:
                done = True
            if slope_total != 0 and not done:
                trialprice -= sum(investor_demands) / slope_total
            else:
                trialprice *= 1 + self.eta * sum(investor_demands)

            slope_total = sum([investors[i].demand_derivative(market_state) for i in range(num_agents)])
            unrestricted_price = trialprice
            if trialprice > self.max_price:
                trialprice = Decimal(self.max_price)
            if trialprice < self.min_price:
                trialprice = Decimal(self.min_price)

            trial_count += 1
            if trial_count < self.max_trials and done is False:
                investor_demands = []
        if trial_count == self.max_trials and done is False:
            is_rationed = True

        if not is_rationed:#abs(sum(investor_demands)) < self.min_excess:
            normalized_demands = investor_demands
        else:
            offers = abs(sum([i for i in investor_demands if i < 0]))
            sum_bids = sum([i for i in investor_demands if i > 0])
            if sum_bids > 0:
                weights = [max(i / sum_bids, 0) for i in investor_demands]
            else:
                weights = [0 for i in investor_demands]
            normalized_demands = []
            for i in range(len(investor_demands)):
                if investor_demands[i] <= 0:
                    normalized_demands.append(investor_demands[i])
                else:
                    normalized_demands.append(weights[i] * offers)
        if zero_excess:
            normalized_demands = list(map(lambda x: x.quantize(Decimal("1.00")), normalized_demands))
            excess = sum(normalized_demands)
            if excess > Decimal(0):
                count = int(excess.quantize(Decimal('1.00')) * 100)
                for i in range(count):
                    ind = random.choice(range(len(normalized_demands)))
                    normalized_demands[ind] -= Decimal(0.01)
            elif excess < 0:
                count = int(-excess.quantize(Decimal('1.00')) * 100)
                for i in range(count):
                    ind = random.choice(range(len(normalized_demands)))
                    normalized_demands[ind] += Decimal(0.01)
        return trialprice, normalized_demands, is_rationed, unrestricted_price

    def find_price(self, dividend, investors, market_state, zero_excess=False):
        num = []
        den = []
        is_rationed = False
        for investor in investors:
            best_rule = investor.select_rule(market_state)
            a, b = best_rule.get_coefs()
            try:
                sigma = best_rule.accuracy
            except TypeError:
                sigma = best_rule.accuracy
            num.append(Decimal(Decimal(b + a * Decimal(dividend)) / Decimal(sigma)))
            den.append((Decimal(a) - Decimal(1) - investor.risk_free) / sigma)
        price = (investors[0].risk_aversion_coef * self.num_shares - sum(num)) / sum(den)
        demands = [i.stock_demand(price, market_state, dividend) for i in investors]
        unrestricted_price = price
        if price <= self.min_price:
            is_rationed = True
            price = self.min_price
        elif price >= self.max_price:
            is_rationed = True
            price = self.max_price
        if not is_rationed:#sum(demands) < self.min_excess:
            normalized_demands = demands
        else:
            offers = abs(sum([i for i in demands if i < 0]))
            sum_bids = sum([i for i in demands if i > 0])
            if sum_bids > 0:
                weights = [max(i / sum_bids, 0) for i in demands]
            else:
                weights = [0 for i in demands]
            normalized_demands = []
            for i in range(len(demands)):
                if demands[i] <= 0:
                    normalized_demands.append(demands[i])
                else:
                    normalized_demands.append(weights[i] * offers)
        if zero_excess:
            normalized_demands = list(map(lambda x: x.quantize(Decimal("1.00")), normalized_demands))
            excess = sum(normalized_demands)
            if excess > Decimal(0):
                count = int(excess.quantize(Decimal('1.00')) * 100)
                for i in range(count):
                    ind = random.choice(range(len(normalized_demands)))
                    normalized_demands[ind] -= Decimal(0.01)
            elif excess < 0:
                count = int(-excess.quantize(Decimal('1.00')) * 100)
                for i in range(count):
                    ind = random.choice(range(len(normalized_demands)))
                    normalized_demands[ind] += Decimal(0.01)

        return price, normalized_demands, is_rationed, unrestricted_price
