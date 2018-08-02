transformed data {
  matrix[2, 2] u;
  u[1, 1] = 1.0; u[1, 2] = 4.0;
  u[2, 1] = 9.0; u[2, 2] = 16.0;
  for (n in 1:2)
    print("u[", n, "] = ", u[n]);
}