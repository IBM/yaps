import numpy as np
from .utils import compare_models


def test_regression_matrix():
    stan_code = """
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

    num_samples = 100
    num_features = 2
    #X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    X = np.random.randint(5, size=(100, 2))
    # y = 1 * x_0 + 2 * x_1 + 3
    y = np.dot(X, np.array([1, 2])) + 3

    data = {'N': num_samples,
            'K': num_features,
            'x': X,
            'y': y}

    compare_models(stan_code, data)

    # if matplotlib is installed (optional, not required), a visual summary and
    # traceplot are available
    # print(fit_stan)
    #import matplotlib.pyplot as plt
    # fit.plot()
    # plt.show()


test_regression_matrix()
