data {
    int<lower=0> N;
    vector[N] x;
    int<lower=0,upper=1> y[N];
}
parameters {
    real alpha;
    real beta;
}
model {
    y ~ bernoulli_logit(alpha + beta * x);
}