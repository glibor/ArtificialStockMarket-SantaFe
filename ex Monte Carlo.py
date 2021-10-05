import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import statsmodels.api as sm


def SimDistributionMC(draws, function):
    """
    Implementa a simulação monte carlo a partir da distribuição uniforme [0,1] de acordo com o capítulo 2 do livro
    Monte Carlo Statistical Methods.
    :param function: generalized inverse cumulative function: função inversa somente para aplicar na amostra da uniforme
    :param reps: number of monte carlo repetitions
    :return:
    """
    vf = np.vectorize(function)
    return vf(draws)


def histogram_plots(x, title="", save=False, densidade=False):
    plt.hist(x=x, bins='auto', color='#0504aa',
             density=densidade)  # plt.hist(x=x, bins='auto', color='#0504aa', density=densidade)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Valor')
    plt.ylabel('Probabilidade')
    if title != "":
        plt.title(title)
    else:
        plt.title("Frequência")
    # plt.title('My Very Own Histogram')
    # plt.text(23, 45, r'$\mu=15, b=3$')
    # Set a clean upper y-axis limit.
    # plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    if save:
        plt.savefig('C:/Users/Pichau/Desktop/Aorta/Captcha Breaker/' + title + '.png')
    else:
        plt.show()


def histogram_plots_true(x, dens, title="", save=False, densidade=False):
    f = np.vectorize(dens)
    plt.hist(x=x, bins='auto', color='#0504aa',
             density=densidade)  # plt.hist(x=x, bins='auto', color='#0504aa', density=densidade)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Valor')
    plt.ylabel('Probabilidade')
    if title != "":
        plt.title(title)
    else:
        plt.title("Frequência")
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 1000)
    p = f(x)
    plt.plot(x, p, 'r', linewidth=1)
    # plt.title('My Very Own Histogram')
    # plt.text(23, 45, r'$\mu=15, b=3$')
    # Set a clean upper y-axis limit.
    # plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    if save:
        plt.savefig('C:/Users/Pichau/Desktop/Aorta/Captcha Breaker/' + title + '.png')
    else:
        plt.show()
    pass


def unif():
    return lambda x: x


def exponential(lam):
    def f(x):
        return -np.log(1 - x) / lam

    return f


def exponential_dens(lam):
    def f(x):
        if x >= 0:
            return lam * np.exp(-lam * x)
        else:
            return x * 0

    return f


def laplace(m, b):
    def f(x):
        if x <= 1 / 2:
            return np.log(2 * x) * b + m
        else:
            return -np.log(2 - 2 * x) * b + m

    return f


def laplace_dens(m, b):
    return lambda x: (1 / (2 * b)) * np.exp(-abs(x - m) / b)


def weibull(k, lam):
    def f(x): return (-lam * np.log(1 - x)) ** (1 / k)

    return f


def weibull_dens(k, lam):
    def f(x):
        if x >= 0:
            return (k / lam) * ((x / lam) ** (k - 1)) * np.exp(-((x / lam) ** k))
        else:
            return 0 * x

    return f


def pareto(x_o, alfa):
    def f(x):
        return x_o / (1 - x) ** (1 / alfa)

    return f


def pareto_dens(x_o, alfa):
    def f(x):
        if x >= x_o:
            return (alfa * np.power(x_o, alfa)) / np.power(x, alfa + 1)
        else:
            return x * 0

    return f


def cauchy(x_0, gama):
    def f(x): return x_0 + gama * np.tan(np.pi * (x - 1 / 2))

    return f


def cauchy_dens(x_0, gama):
    def f(x):
        return (np.pi * gama * (1 + ((x - x_0) / gama) ** 2)) ** -1  # np.arctan((x-x_0)/gama)/np.pi+1/2

    return f


def EV(m, s):
    def f(x): return m - s * np.log(-np.log(x))

    return f


def EV_dens(m, s):
    def f(x):
        return (1/s)*np.exp(-(x - m) / s) * np.exp(-np.exp(-(x - m) / s))

    return f


def arcsine():
    def f(x):
        return (np.sin(x * np.pi / 2)) ** 2

    return f


def arcsine_dens():
    def f(x):
        return (np.pi * np.sqrt(x * (1 - x))) ** -1

    return f


if __name__ == "__main__":
    dicio = {#'Uniforme': [unif(), unif()],
             # 'Exponencial': [exponential(1.5), exponential_dens(1.5)],
             # 'Laplace': [np.vectorize(laplace(0, 1)), laplace_dens(0, 1)],
             # 'Weibull': [weibull(k=2, lam=1), weibull_dens(k=2, lam=1)],
             # 'Pareto': [pareto(1, 10), pareto_dens(1, 10)],
             'Cauchy': [cauchy(0, 0.5), cauchy_dens(0, 0.5)],
             #'Valor extremo': [EV(0, 0.5), EV_dens(0, 0.5)],
             # 'Arcoseno': [arcsine(), arcsine_dens()]
             }
    np.random.seed(0)
    unif_draws = np.random.uniform(low=0.0, high=1.0, size=100)
    for i in dicio:
        plt.clf()
        print(i)
        data = dicio[i][0](unif_draws)
        histogram_plots_true(data, dicio[i][1], i, save=True, densidade=True)
        print("ok!")
