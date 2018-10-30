import pystan
import numpy as np
import yaps
from .utils import compare_fit_objects, global_num_chains,global_num_iterations,global_random_seed


def test_gradient_warn():
    stan_code = """
        data {
            int N;
            vector[N] p;
            int Ngrps;
            int<lower=1, upper=Ngrps> grp_index[N];
        }
        parameters {
            vector<lower=0.0001, upper=100>[Ngrps] sigmaGrp;
            vector<lower=-100, upper=1000>[Ngrps] muGrp;
        }

        model {
            int grpi;
            for (i in 1:N){
                grpi <- grp_index[i];
                p[i] ~ logistic(muGrp[grpi], sigmaGrp[grpi]);
            };
        }
    """

    # Round Trip from Stan to Yaps to Stan
    yaps_code = yaps.from_stan(code_string=stan_code)
    generated_stan_code = yaps.to_stan(yaps_code)

    # Add Data
    num_samples = 10
    X = [63.1, 108.3, 1.0, 46.0, 22.9, 14.8, 28.8, 52.5, 60.1, 81.3]

    data = {'N': num_samples,
            'p': X,
            'Ngrps': 5,
            'grp_index':[1, 1, 1, 1, 1, 1, 2, 3, 4, 5]}

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

if __name__ == "__main__":
    test_gradient_warn()
