data {
  real lb;
}
parameters {
  real<lower=lb> phi;
}