from yaps.lib import *
import yaps as yaps

"""
data {
  int<lower=0> N;
  int<lower=0> K;
  matrix[N, K] x;
  vector[N] y;
}
transformed data {
      matrix[N, K] Q_ast;
      matrix[K, K] R_ast;
      matrix[K, K] R_ast_inverse;
      // thin and scale the QR decomposition
      Q_ast = qr_Q(x)[, 1:K] * sqrt(N - 1);
      R_ast = qr_R(x)[1:K, ] / sqrt(N - 1);
      R_ast_inverse = inverse(R_ast);
    }
parameters {
      real alpha;           // intercept
      vector[K] theta;      // coefficients on Q_ast
      real<lower=0> sigma;  // error scale
}
model {
      y ~ normal(Q_ast * theta + alpha, sigma);  // likelihood
}
generated quantities {
      vector[K] beta;
      beta = R_ast_inverse * theta; // coefficients on x
}
"""

N = yaps.dependent_type_var()
K = yaps.dependent_type_var()


@yaps.model
def regression(N: int(lower=0), K: int(lower=0), x: matrix[N, K], y: vector[N]):
    with transformed_data:
        Q_ast: matrix[N, K]
        R_ast: matrix[K, K]
        R_ast_inverse: matrix[K, K]
        Q_ast = qr_Q(x)[:, 1:K] * sqrt(N - 1)
        R_ast = qr_R(x)[1:K, :] / sqrt(N - 1)
        R_ast_inverse = inverse(R_ast)
    alpha: real
    theta: vector[K]
    sigma: real(lower=0)
    y is normal(Q_ast * theta + alpha, sigma)
    with generated_quantities:
        beta: vector[K]
        beta = R_ast_inverse * theta


print(regression)
