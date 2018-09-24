data {
  int d;
  matrix[d, d] d_m;
}

transformed data {
  vector[d] td = d_m[, 1];
}

model {
}
