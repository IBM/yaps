#include ch02_2_std_normal.stan
parameters {
  real y;
}
model {
  y ~ std_normal();
}
