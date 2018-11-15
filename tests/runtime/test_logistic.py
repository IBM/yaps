import numpy as np
from .utils import compare_models


def test_logistic():
    stan_code = """
        data {
        int<lower=0> N;               // number of items
        int<lower=0> M;               // number of predictors
        int<lower=0,upper=1> y[N];           // outcomes
        row_vector[M] x[N];      // predictors
        }
        parameters {
        vector[M] beta;          // coefficients
        }
        model {
        for (m in 1:M)
            beta[m] ~ cauchy(0.0, 2.5);

        for (n in 1:N)
            y[n] ~ bernoulli(inv_logit(x[n] * beta));
        }
    """

    num_samples = 7
    num_features = 2
    #X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    X = np.array([[1, 1.329799263], [1, 1.272429321], [1, -1.539950042],
                  [1, -0.928567035], [1, -0.294720447], [1, -0.005767173], [1, 2.404653389]])
    # y = 1 * x_0 + 2 * x_1 + 3
    y = np.array([0, 1, 1, 1, 1, 1, 1])
    data = {'N': num_samples,
            'M': num_features,
            'x': X,
            'y': y}

    compare_models(stan_code, data)


if __name__ == "__main__":
    test_logistic()
