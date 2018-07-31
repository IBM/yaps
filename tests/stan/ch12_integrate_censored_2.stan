data {
      int<lower=0> N_obs;
      int<lower=0> N_cens;
      real y_obs[N_obs];
}
parameters {
      real<upper=min(y_obs)> L;
      real mu;
      real<lower=0> sigma;
}
model {
      L ~ normal(mu, sigma);
      y_obs ~ normal(mu, sigma);
      target += N_cens * normal_lcdf(L | mu, sigma);
}