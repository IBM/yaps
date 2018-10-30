import yaps as yaps
from yaps.lib import int, real, parameters, model, uniform, bernoulli
import pystan


@yaps.model
def coin(x: int(lower=0, upper=1)[10]):
    with parameters:
        theta: real(lower=0, upper=1)
    with model:
        theta < ~ uniform(0, 1)
        for i in range(10):
            x[i] < ~ bernoulli(theta)


flips = [0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
print(coin)

fit = yaps.apply(pystan.stan, coin(x=flips),
                iter=1000)
print(fit)
