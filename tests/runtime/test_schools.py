import numpy as np
from .utils import compare_models


def test_schools():
    stan_code = """
    data {
        int<lower=0> J; // number of schools
        real y[J]; // estimated treatment effects
        real<lower=0> sigma[J]; // s.e. of effect estimates
    }
    parameters {
        real mu;
        real<lower=0> tau;
        real eta[J];
    }
    transformed parameters {
        real theta[J];
        for (j in 1:J)
            theta[j] = mu + tau * eta[j];
    }
    model {
        eta ~ normal(0, 1);
        y ~ normal(theta, sigma);
    }
    """

    schools_dat = {'J': 8,
                   'y': np.array([28,  8, -3,  7, -1,  1, 18, 12]),
                   'sigma': np.array([15, 10, 16, 11, 9, 11, 10, 18])}

    compare_models(stan_code, schools_dat)
