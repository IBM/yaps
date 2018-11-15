import numpy as np
from .utils import compare_models


def test_kmeans():
    stan_code = """
        data {
        int<lower=0> N;  // number of data points
        int<lower=1> D;  // number of dimensions
        int<lower=1> K;  // number of clusters
        vector[D] y[N];  // observations
        }
        transformed data {
        real<upper=0> neg_log_K;
        neg_log_K = -log(K);
        }
        parameters {
        vector[D] mu[K]; // cluster means
        }
        transformed parameters {
        real<upper=0> soft_z[N, K]; // log unnormalized clusters
        for (n in 1:N)
            for (k in 1:K)
            soft_z[n, k] = neg_log_K
                - 0.5 * dot_self(mu[k] - y[n]);
        }
        model {
        // prior
        for (k in 1:K)
                mu[k] ~ normal(0, 1);
        // likelihood
        for (n in 1:N)
                target += log_sum_exp(soft_z[n]);
        }
    """

    num_samples = 6
    num_features = 2
    X = np.array([[1, 2], [1, 4], [1, 0], [4, 2], [4, 4], [4, 0]])
    num_clusters = 2

    data = {'N': num_samples,
            'D': num_features,
            'K': num_clusters,
            'y': X}

    compare_models(stan_code, data)


if __name__ == "__main__":
    test_kmeans()
