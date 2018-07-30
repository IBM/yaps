data {
    int<lower=0> N;
    int<lower=0> K;
    matrix[N, K] x;
    vector[N] y;
}
parameters {
    real alpha;
    vector[K] beta;
    real<lower =0> sigma;
}
model {
      y ~ normal(x * beta + alpha, sigma);
}