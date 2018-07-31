data{
  int N;
  real y[N];
}
parameters{
  real mu;
  real tau;
}
transformed parameters{
  real sigma = pow(tau,-0.5);
}
model{
  tau ~ gamma(0.1,0.1); mu ~ normal(0,1);
  y ~ normal(mu,sigma);
}
generated quantities{
  real v = pow(sigma,2);
}
