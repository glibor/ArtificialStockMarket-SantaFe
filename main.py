import random
from decimal import Decimal
import datetime

import pywhatkit as pwkt

from Agents import Investor, Specialist, Rule
from Market import MarketInfo
from Simulation import Simulation

param = {"genetic_param": 0.9,
         "param": "valor_do_param"}

# number_agents = 100
# a = Simulation(25, 20)
# a.initialiaze_agents()
# pri = a.MainSimulation(progress=True, price_setting='clearing')


if __name__ == '__main__':
    for i in [k for k in range(1)]:
        a = Simulation(20, 500)
        pri = a.MainSimulation(progress=1, price_setting='auction', new_agents=False)

