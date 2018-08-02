data {
  int<lower=1> N;
  real y[N];
}
parameters {
  real<lower=min(y), upper=max(y)> phi;
}