from yaps import parse_model
from yaps.lib import int, real, parameters, model, uniform, bernoulli


def coin_model_py(x: int(lower=0, upper=1)[10]):
    with parameters:
        theta: real(lower=0, upper=1)
    with model:
        theta < ~ uniform(0, 1)
        for i in range(10):
            x[i] < ~ bernoulli(theta)


parse_model(coin_model_py)

print('----------------')


def coin_model_py2(x: int(lower=0, upper=1)[10]):
    theta: real(lower=0, upper=1) is uniform(0, 1)
    for i in range(10):
        x[i] is bernoulli(theta)


parse_model(coin_model_py2)
