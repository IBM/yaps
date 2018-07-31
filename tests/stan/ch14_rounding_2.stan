data {
    int<lower=0> N;
    vector[N] y;
}
parameters {
    real mu;
    real<lower=0> sigma_sq;
    vector<lower=(-0.5), upper=0.5>[N] y_err;
}
transformed parameters {
    real<lower=0> sigma;
    vector[N] z;
    sigma = sqrt(sigma_sq);
    z = y + y_err;
}
model {
    target += -2 * log(sigma);
    z ~ normal(mu, sigma);
}