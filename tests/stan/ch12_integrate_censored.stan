data {
    int<lower=0> N_obs;
    int<lower=0> N_cens;
    real y_obs[N_obs];
    real<lower=max(y_obs)> U;
}
parameters {
    real mu;
    real<lower=0> sigma;
}
model {
    y_obs ~ normal(mu, sigma);
    target += N_cens * normal_lccdf(U, mu, sigma);
}
