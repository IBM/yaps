data {
  int<lower=0> N;
  real x[N];
  real y[N];
}
parameters {
  real alpha;
  real beta;
  real<lower=0> sigma;  // outcome noise
}
model {
  y ~ normal(alpha + beta * x, sigma);
  alpha ~ normal(0, 10);
  beta ~ normal(0, 10);
  sigma ~ cauchy(0, 5);
}