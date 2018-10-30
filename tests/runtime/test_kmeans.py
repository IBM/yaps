import pystan
import numpy as np
import yaps
from .utils import compare_fit_objects, global_num_chains,global_num_iterations,global_random_seed


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

    # Round Trip from Stan to Yaps to Stan
    yaps_code = yaps.from_stan(code_string=stan_code)
    generated_stan_code = yaps.to_stan(yaps_code)

    # Add Data, from http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
    num_samples = 6
    num_features = 2
    X = np.array([[1, 2], [1, 4], [1, 0], [4, 2], [4, 4], [4, 0]])
    num_clusters = 2

    data = {'N': num_samples,
            'D': num_features,
            'K': num_clusters,
            'y': X}

    # Compile and fit
    sm1 = pystan.StanModel(model_code=str(stan_code))
    fit_stan = sm1.sampling(data=data, iter=global_num_iterations, chains=global_num_chains, seed=global_random_seed)

    # Compile and fit
    sm2 = pystan.StanModel(model_code=str(generated_stan_code))
    fit_generated_stan = sm2.sampling(data=data, iter=global_num_iterations, chains=global_num_chains, seed=global_random_seed)

    compare_fit_objects(fit_stan, fit_generated_stan)

    # if matplotlib is installed (optional, not required), a visual summary and
    # traceplot are available
    #print(fit_stan)
    #import matplotlib.pyplot as plt
    #fit.plot()
    #plt.show()

#if __name__ == "__main__":
test_kmeans()
