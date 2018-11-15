import numpy as np
from .utils import compare_models


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

    num_samples = 10
    X = np.array([63.1, 108.3, 1.0, 46.0, 22.9, 14.8, 28.8, 52.5, 60.1, 81.3])

    data = {'N': num_samples,
            'p': X,
            'Ngrps': 5,
            'grp_index': np.array([1, 1, 1, 1, 1, 1, 2, 3, 4, 5])}

    compare_models(stan_code, data)


if __name__ == "__main__":
    test_gradient_warn()
