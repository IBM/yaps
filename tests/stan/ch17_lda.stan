data {
  int<lower=2> K;
  int<lower=2> V;
  int<lower=1> M;
  int<lower=1> N;
  int<lower=1,upper=V> w[N];
  int<lower=1,upper=M> doc[N];  // doc ID for word n
  vector<lower=0>[K] alpha;     // topic prior
  vector<lower=0>[V] beta;      // word prior
}
parameters {
  simplex[K] theta[M];
  simplex[V] phi[K];
} model {
// topic dist for doc m
// word dist for topic k
for (m in 1:M)
  theta[m] ~ dirichlet(alpha);  // prior
for (k in 1:K)
  phi[k] ~ dirichlet(beta);     // prior
for (n in 1:N) {
  real gamma[K];
  for (k in 1:K)
    gamma[k] = log(theta[doc[n], k]) + log(phi[k, w[n]]);
  target += log_sum_exp(gamma);  // likelihood;
  }
}