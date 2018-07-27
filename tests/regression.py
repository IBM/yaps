import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'yaps')))

from yaps.lib import *
import yaps as yaps

"""
data {
      int<lower=0> N;
      vector[N] x;
      vector[N] y;
    }
parameters {
      real alpha;
      real beta;
      real<lower=0> sigma;
}
model {
      y ~ normal(alpha + beta * x, sigma);
    }
"""

N = yaps.dependent_type_var()


@yaps.model
def regression(N: int(lower=0), x: vector[N], y: vector[N]):
    alpha: real
    beta: real
    sigma: real(lower=0)
    y is normal(alpha + beta * x, sigma)


print(regression)
