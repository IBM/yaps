import src.py2ir as p2ir
from src.lib import *


def coin_model_py(x: int(lower=0, upper=1)[10]):
    with parameters:
        theta: real(lower=0, upper=1)
    with model:
        theta < ~ uniform(0, 1)
        for i in range(10):
            x[i] < ~ bernoulli(theta)


p2ir.parse_model(coin_model_py)
