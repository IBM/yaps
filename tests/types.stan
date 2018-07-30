data {  int AA[5];  matrix<lower=0>[5, 6] A[6];
  matrix[5, 6] B[6];
  matrix[5, 6] C[6, 7];
  matrix<lower=0>[5, 6] D;
  simplex[5] E;
}
parameters {
  simplex<lower=0>[5] F[5, 6];
  simplex[5] G;
  simplex<lower=0>[] H;
  int<upper=5> I[3];
  int<upper=5> J;
  vector[12] K = {1,2,4,4,5,6,7,78};
  int L[6];
  real alpha;
}