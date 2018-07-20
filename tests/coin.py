import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'yaps')))

from yaps import parse_model
from yaps.lib import int, real, uniform, bernoulli


def coin_model_py(x: int(lower=0, upper=1)[10]):
    theta: real(lower=0, upper=1) is uniform(0, 1)
    for i in range(10):
        x[i] is bernoulli(theta)


parse_model(coin_model_py)
