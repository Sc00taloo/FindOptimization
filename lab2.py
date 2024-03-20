import numpy as np
from scipy.optimize import minimize
def f(x1, x2):
    return 2 * x1 ** 2 + 3 * x2 **2 + 4 * x1*x2 - 6 * x1 - 3 * x2
def simplex_method(x,y):
    points = []
    def fun(x_i):
        x1 = x_i[0]
        x2 = x_i[1]
        return 2 * x1 ** 2 + 3 * x2 **2 + 4 * x1*x2 - 6 * x1 - 3 * x2
    def callback(x_w):
        g_list = np.ndarray.tolist(x_w)
        g_list.append(fun(x_w))
        points.append(g_list)

    #диапазон поиска
    b = (0, float("inf"))
    bounds = (b, b)
    #начальная точка
    x0 = (x, y)
    con = {'type': 'eq', 'fun': fun}
    #основной вызов
    res = minimize(fun, x0, method="SLSQP", bounds=bounds,constraints=con, callback=callback)

    glist = np.ndarray.tolist(res.x)
    glist.append(res.fun)
    points.append(glist)

    for iteration, point in enumerate(points):
        yield iteration, point