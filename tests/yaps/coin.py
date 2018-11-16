from yaps.lib import int, real, uniform, bernoulli
import yaps as yaps
import numpy as np


@yaps.model
def coin(x: int(lower=0, upper=1)[10]):
    theta: real(lower=0, upper=1) is uniform(0, 1)
    for i in range(1, 11):
        x[i] is bernoulli(theta)


coin.graph
print(coin)

flips = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 1])

constrained_coin = coin(x=flips)
constrained_coin.sample(data=constrained_coin.data)
theta_mean = constrained_coin.posterior.theta.mean()
print("mean of theta: {:.3f}".format(theta_mean))
