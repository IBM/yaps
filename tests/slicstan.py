import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'yaps')))

from yaps import parse_model
from yaps.lib import int, real, transformed_parameters, generated_quantities, gamma, normal


def slicstan(N: int, y: real(lower=0, upper=1)[10]):
    mu: real
    tau: real
    with transformed_parameters:
        sigma: real = pow(tau, -0.5)
    tau is gamma(0.1, 0.1)
    mu is normal(0, 1)
    y is normal(mu, sigma)
    with generated_quantities:
        v: real = pow(sigma, 2)


parse_model(slicstan)
