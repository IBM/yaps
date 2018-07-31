data {
  int<lower=0> N;
  vector[2] y[N];
  real<lower=0> var1; real<lower=0> var2;
}
transformed data {
  real<lower=0> max_cov = sqrt(var1 * var2);
  real<upper=0> min_cov = -max_cov;
}
parameters {
  vector[2] mu;
  real<lower=min_cov, upper=max_cov> cov;
}
transformed parameters {
  matrix[2, 2] Sigma;
  Sigma[1, 1] = var1; Sigma[1, 2] = cov;
  Sigma[2, 1] = cov; Sigma[2, 2] = var2;
}
model {
  y ~ multi_normal(mu, Sigma);
}
