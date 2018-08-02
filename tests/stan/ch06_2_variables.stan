data {
  int<lower=0> N; // unmodeled data
  real y[N]; // modeled data
  real mu_mu; // config. unmodeled param
  real<lower=0> sigma_mu; // config. unmodeled param
}
transformed data {
  real<lower=0> alpha; // const. unmodeled param
  real<lower=0> beta; // const. unmodeled param
  alpha = 0.1;
  beta = 0.1;
}
parameters {
  real mu_y; // modeled param
  real<lower=0> tau_y; // modeled param
}
transformed parameters {
  real<lower=0> sigma_y; // derived quantity (param)
  sigma_y = pow(tau_y, -0.5);
}
model {
  tau_y ~ gamma(alpha, beta);
  mu_y ~ normal(mu_mu, sigma_mu);
  for (n in 1:N)
    y[n] ~ normal(mu_y, sigma_y);
}
generated quantities {
  real variance_y; // derived quantity (transform)
  variance_y = sigma_y * sigma_y;
}