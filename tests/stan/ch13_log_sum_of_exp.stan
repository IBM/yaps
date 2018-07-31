parameters {
  real y;
}
model {
 target += log_sum_exp(log(0.3) + normal_lpdf(y | -1, 2),
                       log(0.7) + normal_lpdf(y | 3, 1));
}