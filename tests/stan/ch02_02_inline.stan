functions {
  real std_normal_lpdf(vector y) {
    return -0.5 * y' * y;
  }
}
parameters {
  real y;
}
model {
  y ~ std_normal();
}
