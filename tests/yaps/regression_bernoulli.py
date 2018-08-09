from yaps.lib import *
import yaps as yaps

"""
data {
    int<lower=0> N;
    vector[N] x;
    int<lower=0,upper=1> y[N];
}
parameters {
    real alpha;
    real beta;
}
model {
    y ~ bernoulli_logit(alpha + beta * x);
}
"""

N = yaps.dependent_type_var()


@yaps.model
def regression(N: int(lower=0), x: vector[N], y: vector(lower=0, upper=1)[N]):
    alpha: real
    beta: real
    y is bernoulli_logit(alpha + beta * x)


print(regression)
