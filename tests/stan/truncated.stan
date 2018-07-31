data {
    int<lower=0> N;
    real U;
    real<upper=U> y[N];
}
parameters {
    real mu;
    real<lower=0> sigma;
}
model {
    for (n in 1:N)
        y[n] ~ normal(mu, sigma) T[,U];
}
