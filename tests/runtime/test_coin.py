import numpy as np
from .utils import compare_models


def test_coin():
    stan_code = """
       data {
       int x[10];
       }
       parameters {
       real theta;
       }
       model {
       theta ~ uniform(0.1,1.0);
       for (i in 1:10){
           x[i] ~ bernoulli(theta);
       }
       }
   """

    data = {'x': np.array([0, 1, 1, 0, 1, 1, 0, 0, 0, 1])}
    compare_models(stan_code, data)


if __name__ == "__main__":
    test_coin()
