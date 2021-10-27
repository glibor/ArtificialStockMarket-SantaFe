import math


class Derivative(object):
    def __init__(self, f, h=1E-5):
        self.f = f
        self.h = float(h)

    def __call__(self, x):
        f, h = self.f, self.h  # make short forms
        return (f(x + h) - f(x)) / h


class Sum:

    def __init__(self, regra, first, last):
        self.func = regra
        self.first = first
        self.last = last
        self.f_sen = lambda x, k: (x ** (2 * k + 1)) * (((-1) ** k) / math.factorial(2 * k + 1))
        self.f_exp = lambda x, k: ((x ** k) / math.factorial(k))

    def __call__(self, x):
        valor = 0
        for k in range(self.first, self.last + 1):
            valor += self.func(x, k)
        return valor


class MinMax:

    def __init__(self, f, a, b, n):
        """
         f: função
        a: início do domínio nos reais
        b: fim do domínio nos reais
        n: quantos pontos do domínios devem ser avaliados
        """
        self.f = f
        self.a = a
        self.b = b
        self.n = n
        self._find_extrema()

    def __str__(self):
        print("Extremos da função")
        print("------------------")
        print("Máxmimos globais: ", self.maximos_globais)
        print("Mínimos globais:", self.minimos_globais)
        print("Máxmimos locais:", self.maximos_locais)
        print("Mínmimos locais:", self.minimos_locais)
        return "------------------"

    def _find_extrema(self):
        maximos = []
        minimos = []
        grid = [self.a + i * (self.b - self.a) / self.n for i in range(1, self.n + 1)]
        grid = [self.a] + grid
        for i, value in enumerate(grid):
            if 0 < i < len(grid) - 1:
                if self.f(value) >= self.f(grid[i - 1]) and self.f(value) >= self.f(grid[i + 1]):
                    maximos.append(value)
                if self.f(value) <= self.f(grid[i - 1]) and self.f(value) <= self.f(grid[i + 1]):
                    minimos.append(value)
            elif i == 0:
                if self.f(value) >= self.f(grid[i + 1]):
                    maximos.append(value)
                if self.f(value) <= self.f(grid[i + 1]):
                    minimos.append(value)
            else:
                if self.f(value) >= self.f(grid[i - 1]):
                    maximos.append(value)
                if self.f(value) <= self.f(grid[i - 1]):
                    minimos.append(value)
        f_max = max(list(map(self.f, maximos)))
        f_min = min(list(map(self.f, minimos)))
        self.grid = grid
        self.maximos_locais = maximos
        self.minimos_locais = minimos
        self.maximos_globais = [i for i in maximos if self.f(i) >= f_max]
        self.minimos_globais = [i for i in minimos if self.f(i) <= f_min]

    def refine_extrema(self, n_refinos=5):

        a, b, grid = self.a, self.b, self.grid
        maximos_refinados = []
        minimos_refinados = []
        df = Derivative(self.f)
        for i in self.maximos_globais:
            new_max = i
            index_0 = self.grid.index(i)
            if i != a and i != b:
                q = grid[index_0-1]
                Q = grid[index_0+1]
                for _ in range(0, n_refinos):
                    new_max = (q+Q)/2
                    if abs(df(new_max)) <= 1E-6:
                        break
                    elif df(new_max) > 0:
                        q = new_max
                    elif df(new_max) < 0:
                        Q = new_max
                maximos_refinados.append(new_max)

        for i in self.minimos_globais:
            new_min = i
            index_0 = self.grid.index(i)
            if i != a and i != b:
                q = grid[index_0 - 1]
                Q = grid[index_0 + 1]
                for _ in range(0, n_refinos):
                    new_min = (q + Q) / 2
                    if abs(df(new_min)) <= 1E-5:
                        break
                    elif df(new_min) > 0:
                        Q = new_min
                    elif df(new_min) < 0:
                        q = new_min
                minimos_refinados.append(new_min)
        return {"minimos": minimos_refinados, "maximos": maximos_refinados}

    def get_global_maxima(self):
        return [[i, self.f(i)] for i in self.maximos_globais]

    def get_global_minima(self):
        return [[i, self.f(i)] for i in self.minimos_globais]

    def get_local_maxima(self):
        return [[i, self.f(i)] for i in self.maximos_locais]

    def get_local_minima(self):
        return [[i, self.f(i)] for i in self.minimos_locais]


if __name__ == "__main__":
    def func(x):
        return (x)**2
    m = MinMax(func, -1, 2, 1000)
    m_r = m.refine_extrema(5)
    print(m)
    print(m_r)
