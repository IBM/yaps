from yaps.lib import *
import yaps as yaps
import pystan

N = yaps.dependent_type_var()
@yaps.model
def slicstan(N: int, y: real(lower=0, upper=1)[N]):
    tau: real is gamma(0.1, 0.1)
    mu: real is normal(0, 1)
    with transformed_parameters:
        sigma: real = pow(tau, -0.5)
    y is normal(mu, sigma)
    with generated_quantities:
        v: real = pow(sigma, 2)


print(slicstan)
y = [0.5,0.5,0.5,0.5,0.5]
fit = yaps.apply(pystan.stan, slicstan(N=len(y),y=y),iter=1000)
print(fit)
