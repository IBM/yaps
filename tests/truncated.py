import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'yaps')))

from yaps.lib import *
import yaps as yaps

N = yaps.dependent_type_var()
U = yaps.dependent_type_var()


@yaps.model
def truncature(N: int(lower=0), U: real, y: real(upper=U)[N]):
    mu: real
    sigma: real(lower=0)
    for n in range(1 - 1, N):
        y[n] is normal(mu, sigma).T[:, U]


print(truncature)
