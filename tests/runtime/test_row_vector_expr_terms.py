import pystan
import numpy as np
import yaps
from .utils import compare_fit_objects, global_num_chains,global_num_iterations,global_random_seed


def test_row_vector_expr_terms():
    stan_code = """
        functions {

        vector foo(int d) {
            vector[3] result = [10.1, 11*3.0, d]';
            return result;
        }

        row_vector bar() {
            row_vector[2] result = [7, 8];
            return result;
        }

        }
        data {
        real x;
        real y;
        }
        transformed data {
        vector[3] td_v1 = [ 21, 22, 23]';
        row_vector[2] td_rv1 = [ 1, 2];
        td_rv1 = [ x, y];
        td_rv1 = [ x + y, x - y];
        td_rv1 = [ x^2, y^2];
        td_v1 = foo(1);
        td_rv1 = bar();
        }
        parameters {
        real z;
        }
        transformed parameters {
        vector[3] tp_v1 = [ 41, 42, 43]';
        row_vector[2] tp_rv1 = [ 1, x];
        tp_v1 = foo(1);
        tp_v1 = [ 51, y, z]';
        tp_rv1 = [ y, z];
        tp_rv1 = bar();
        }
        model {
        z ~ normal(0,1);
        }
        generated quantities {
        vector[3] gq_v1 = [1, x, y]';
        row_vector[3] gq_rv1 = [1, x, y];
        row_vector[3] gq_rv2 = [1, x, z];
        gq_v1 = foo(1);
        }
    """

    # Round Trip from Stan to Yaps to Stan
    yaps_code = yaps.from_stan(code_string=stan_code)
    generated_stan_code = yaps.to_stan(yaps_code)

    # Add Data
    x = 56.789
    y = 98.765
    data = {'x':x, 'y':y}

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
    test_row_vector_expr_terms()
