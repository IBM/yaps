parameters {
  real<lower=0> y_inv;
}
transformed parameters {
  real<lower=0> y;
  y = 1 / y_inv; // change variables
}
model {
  y ~ gamma(2,4);
  target += -2 * log(y_inv); // Jacobian adjustment;
}