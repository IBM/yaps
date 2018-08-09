from yaps.lib import *
import yaps as yaps

"""
data {
    int<lower=0> N;
    int<lower=0> K;
    matrix[N, K] x;
    vector[N] y;
}
parameters {
    real alpha;
    vector[K] beta;
    real<lower =0> sigma;
}
model {
      y ~ normal(x * beta + alpha, sigma);
}
"""

N = yaps.dependent_type_var()
K = yaps.dependent_type_var()


@yaps.model
def regression(N: int(lower=0), K: int(lower=0), x: matrix[N, K], y: vector[N]):
    alpha: real
    beta: vector[K]
    sigma: real(lower=0)
    y is normal(x * beta + alpha, sigma)


print(regression)
