data {
    int<lower=0> M;
    int<lower=0> C;
    int<lower=0,upper=min(M,C)> R;
}
parameters {
    real<lower=(C - R + M)> N;
}
model {
    R ~ binomial(C, M / N);
}