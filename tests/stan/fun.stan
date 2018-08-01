functions {
  void f(int x);

  real id(real x) {
    return x;
  }

  void swap(real x, real y) {
    real aux = x;
    x = y;
    y = x;
  }

}