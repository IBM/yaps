data {
    int<lower=0> N;
    vector[N] y;
}
parameters {
    real mu;
    real<lower=0> sigma_sq;
}
transformed parameters {
    real<lower=0> sigma;
    sigma = sqrt(sigma_sq);
}
model {
    target += -2 * log(sigma);
    for (n in 1:N)
      target += log(Phi((y[n] + 0.5 - mu) / sigma)
                    - Phi((y[n] - 0.5 - mu) / sigma));
}
