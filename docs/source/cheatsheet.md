# Yaps Modeling Language

A yaps model is a python function prefixed by the `@yaps.model` decorator

```python
import yaps
from yaps.lib import int, real, uniform, bernoulli

@yaps.model
def coin(x: int(lower=0, upper=1)[10]):
    theta: real(lower=0, upper=1) <~ uniform(0, 1)
    for i in range(10):
        x[i] <~ bernoulli(theta)
```

Types definition, e.g., `int` and `real`, and Stan function are defined in `yaps.lib`.

We list below examples of Yaps code with the corresponding Stan code.

## Comments

```python
# This is a comment
x <~ Normal(0,1) # This is a comment
```

## Data Types and Variable Declarations
```python
x: int                                   # int x;
x: real                                  # real x;

x: real[10]                              # real x[10];
m: matrix[6,7] [3,3]                     # matrix[3,3] m[6,7];

N: int(lower=1)                          # int<lower=1> N;
log_p: real(upper=0)                     # real<upper=0> log_p;
rho: vector(lower=-1,upper=1)[3]         # vector<lower=-1,upper=1>[3] rho;

mu: vector[7][3]                         # vector[7] mu[3];
mu: matrix[7,2] [15,12]                  # matrix[7,2] mu[15,12];

x = w[5]                                 # x = w[5];
c = a[1,3]                               # c = a[1,3];
a: matrix[3,2] = 0.5 * (b + c)           # matrix[3,2] a = 0.5 * (b + c);
```

## Expressions

```python
m1: matrix[3,2] = [[1,2],[3,4],[5,6]]    # matrix[3,2] m1 = [[1,2],[3,4],[5,6]];
vX: vector[2] = [1,10].transpose         # vector[2] vX = [1,10]';
a: int[3] = {1,10,1000}                  # int a[3] = {1,10,100};
b: int[2,3] = {{1,2,3},{4,5,6}}          # int b[2,3] = {{1,2,3},{4,5,6}};

3.0+0.14
-15
2*3+1
(x-y)/2.0
(n*(n+1))/2
x/n
m%n

3**2                                     # 3^2
c = a.pmult(b)                           # c = a .* b
c = a.pdiv(b)                            # c = a ./ b
b if a else c                            # a?b:c

x[4]
x[4,:]                                   # x[4,] or x[4,:]
```

## Statements

```python
target += -0.5 * y * y                   # target += -0.5 * y * y;
y <~ normal(mu, sigma)                   # y ~ normal(mu,sigma);
y is normal(mu, sigma)                   # y ~ normal(mu,sigma);
y <~ normal(0,1).T[-0.5, 2.1]            # y ~ normal(0, 1) T[-0.5, 2.1];

for n in range(N): ...                   # for (n in 1:N) {...}
while cond: ...                          # while (cond) {...}
if cond: ...                             # if (cond) {...}
else: ...                                # else {...}

break                                    # break;
continue                                 # continue;
pass                                     # //nothing
```

## Program Blocks

- Data are the keyword argument of the model.
- Top-level declarations are parsed as parameters.
- Top-level statements defined the model.

```python
def model(x: real):                      # data {int x;}
  mu: real                               # parameters {real mu;}
  x <~ normal(mu,1)                      # model { x ~ normal(mu, 1)}
```

Yaps also supports a fully annotated syntax where blocks are introduced via python `with` statements

```python
with functions: ...                      # function {...}
with transformed_data                    # transformed data {...}
with parameters: ...                     # parameters {...}
with transformed_parameters: ...         # transformed parameters {...}
with model: ...                          # model {...}
with generated quantities: ...           # generated quantities {...}
```

## Function Definitions

User defined functions must be defined inside the model in the `functions` block. Their syntax follows Python syntax with type annotations

```python
with functions:                          # funtions {
    def succ(x: int) -> int:             #   int succ(int x) {
        return x + 1                     #     return x + 1;
                                         #   }
                                         # }
```
