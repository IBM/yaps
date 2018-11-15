import numpy as np
from .utils import compare_models


def test_vectorized_probability():
    stan_code = """
        data {
        int<lower=1> K;
        int<lower=1> N;
        matrix[N, K] x;
        vector[N] y;
        }
        parameters {
        vector[K] beta;
        }
        model {
        y ~ normal(x * beta, 1);
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


if __name__ == "__main__":
    test_vectorized_probability()
