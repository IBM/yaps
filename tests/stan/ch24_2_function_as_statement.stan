functions {
  void pretty_print_tri_lower(matrix x) {
  if (rows(x) == 0) {
    print("empty matrix");
    return ;
  }
  print("rows=", rows(x), " cols=", cols(x));
  for (m in 1:rows(x))
    for (n in 1:m)
      print("[", m, ",", n, "]=", x[m, n]);
  }
}