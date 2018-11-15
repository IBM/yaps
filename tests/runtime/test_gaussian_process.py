import numpy as np
from .utils import compare_models


def test_gaussian_process():
    stan_code = """
        data {
        int<lower=1> N;
        real x[N];
        }
        transformed data {
        matrix[N, N] K;
        vector[N] mu = rep_vector(0, N);
        for (i in 1:(N - 1)) {
            K[i, i] = 1 + 0.1;
            for (j in (i + 1):N) {
            K[i, j] = exp(-0.5 * square(x[i] - x[j]));
            K[j, i] = K[i, j];
            }
        }
        K[N, N] = 1 + 0.1;
        }
        parameters {
        vector[N] y;
        }
        model {
        y ~ multi_normal(mu, K);
        }
    """

    num_samples = 6
    X = np.array([5, 6, 1, 0, 9, 10])

    data = {'N': num_samples,
            'x': X}

    compare_models(stan_code, data)


if __name__ == "__main__":
    test_gaussian_process()
