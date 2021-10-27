import random
import time
import logging
from decimal import Decimal
import pickle
import csv

import progressbar
import numpy as np

from Agents import Investor, Specialist, Rule
from Market import MarketInfo, Stock

"""
num_shares = 100
init_price = 80

dividend_startvalue = 10
rho = 1
noise_sd = 0.5
d_bar = 5
interest_rate = 0.02
init_holding = 1
initialcash = 20000
theta = 75
gene_length = 64
risk_coef = 0.5
num_strategies = 80

max_stockprice = 200
min_stockprice = 0.01
min_excess = 0.005
eta = 0.005
specialist_iterations = 10

"""


class Simulation:
    """
    classe que implementa a simulação em si, com os passos e registros.

    """

    def __init__(self, n_agents, n_steps, csv_filepath='output/price.csv', initial_price=80, initial_dividend=10,
                 ga_frquency=10, genetic_param=0.9):
        """


        :param genetic_param:
        :param n_agents:
        :param n_steps:
        :param initial_price:
        :param initial_dividend:
        :param ga_frquency:
        """
        self.n_agents = n_agents
        self.n_steps = n_steps
        self.ga_frquency = ga_frquency
        self.genetic_param = genetic_param
        self.investors = None
        self.specialist = None
        self.market = None
        self.initial_price = initial_price
        self.initial_dividend = initial_dividend
        self.stock = Stock(initial_price=initial_price,
                           initial_dividend=initial_dividend,
                           dividend_mean=10,
                           revision_speed=0.95,
                           dividend_error_var=0.075)
        self.csv_filepath = csv_filepath

    def MainSimulation(self, progress=False, price_setting="clearing", new_agents=False):
        """
        Executa a simulação com base nos parâmetros
        :return:
        """
        if new_agents:
            self.initialiaze_agents()
        else:
            self.load_agents()
            print("Agents loaded sucessfully!")
        if progress:
            step_list = progressbar.progressbar(range(self.n_steps))
        else:
            step_list = range(self.n_steps)
        with open(self.csv_filepath, mode='a', newline='') as data_file:
            for step in step_list:
                self.stock.update_dividend()
                dividend = self.stock.current_dividend
                if step != 0:
                    last_price = Decimal(self.market.price_history[-1])
                else:
                    last_price = Decimal(80)
                    dividend = Decimal(10)
                    self.market.write_step(step, last_price, dividend, 0, 0, 0, 0, 0, file_obj=data_file, header=True)
                    self.market.update_history(last_price, dividend)
                if price_setting == "auction":
                    price, demands, is_rationed, unrestricted_price = self.specialist.calculate_demands(
                        last_price=last_price,
                        last_dividend=dividend,
                        investors=self.investors,
                        market_state=self.market.current_state,
                        zero_excess=False)
                elif price_setting == 'clearing':
                    price, demands, is_rationed, unrestricted_price = self.specialist.find_price(dividend,
                                                                                                 self.investors,
                                                                                                 self.market.current_state,
                                                                                                 False)
                else:
                    Exception('Undefined price setting method')

                # print(demands)
                for ind, agent in enumerate(self.investors):
                    agent.update_portifolio(demands[ind], price, dividend=0)
                    for rule in agent.trading_rules:
                        if rule.is_active(self.market.current_state) and step != 0:
                            rule.update_fitness_accuracy(price, last_price,
                                                         dividend,
                                                         self.market.dividend_history[-1], 75)
                    agent.sort_rules_by_fitness()
                    agent.update_median_accuracy()
                    # best_rule = agent.select_rule(market_state=self.market.current_state)
                    # agent.write_to_df(step, agent.cash, agent.stock_qty, 0, best_rule.specificity, best_rule._alpha,
                    #                  best_rule._beta, best_rule.accuracy[-1])
                    if (step % self.ga_frquency) == 0 and step != 0:
                        agent.genetic_algo(self.genetic_param)

                self.market.write_step(step, price, dividend, 0, 0, is_rationed, unrestricted_price, sum(demands),
                                       file_obj=data_file)

                self.market.update_history(price, dividend)
                self.market.update_info_state(step)
                self.market.unburden_history()
        self.save_agents()
        print("Processo concluído")
        return self.market.price_history

    def initialiaze_agents(self):
        agents = []
        for _ in range(self.n_agents):
            rules = []
            for i in range(100):
                watch = random.choices([0, 1, 2], [1, 1, 18], k=64)
                rules.append(Rule(watch_list=watch, alpha=random.uniform(0.7, 1.2), beta=random.uniform(-10, 19)))
            agents.append(Investor(rules))
        self.investors = agents
        self.specialist = Specialist(max_trials=6,
                                     max_price=200,
                                     min_price=.01,
                                     num_shares=len(agents) + 1,  # num_shares=sum([ag.stock_qty for ag in agents]),
                                     min_excess=10 ** -3,
                                     eta=0.005)
        self.market = MarketInfo(dividend_mean=10)

    def save_agents(self):
        agents = self.investors
        with open('StoredAgents/Investors.pickle', mode='wb') as ag:
            pickle.dump(agents, ag)

    def load_agents(self):
        with open('StoredAgents/Investors.pickle', mode='rb') as ag:
            self.investors = pickle.load(ag)
        for inv in self.investors:
            inv.stock_qty = 1
            inv.cash = 20000
            for j in range(len(inv.trading_rules)):
                if type(inv.trading_rules[j].accuracy) is list:
                    if inv.trading_rules[j].accuracy[-1] is not None:
                        inv.trading_rules[j].accuracy = inv.trading_rules[j].accuracy[-1]
        self.specialist = Specialist(max_trials=6,
                                     max_price=500,
                                     min_price=.01,
                                     num_shares=sum([inv.stock_qty for inv in self.investors]),
                                     # num_shares=sum([ag.stock_qty for ag in agents]),
                                     min_excess=10 ** -3,
                                     eta=0.005)
        self.market = MarketInfo(dividend_mean=10)
