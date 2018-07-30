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
      Q_ast = qr_Q(x)[, 1:K] * sqrt(N - 1);
      R_ast = qr_R(x)[1:K, ] / sqrt(N - 1);
      R_ast_inverse = inverse(R_ast);
    }
parameters {
      real alpha;
      vector[K] theta;
      real<lower=0> sigma;
}
model {
      y ~ normal(Q_ast * theta + alpha, sigma);
}
generated quantities {
      vector[K] beta;
      beta = R_ast_inverse * theta;
}