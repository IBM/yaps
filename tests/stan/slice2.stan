data {
  int n_age;
}

transformed parameters {
  simplex[n_age + 1] pr_a;
  pr_a[n_age + 1] = 1 - sum(pr_a[:n_age]);
}

model {
}