# YAPS

Yaps is a new surface language for [Stan](http://mc-stan.org/). It allows
to write Stan programs using Python syntax. For example, consider the
following Stan program:
```stan
data {
  int<lower=0,upper=1> x[10];
}
parameters {
  real<lower=0,upper=1> theta;
}
model {
  theta ~ uniform(0,1);
  for (i in 1:10)
    x[i] ~ bernoulli(theta);
}
```
It can be rewritten in Python has follows:
```python
import yaps
from yaps.lib import *

@yaps.model
def coin(x: int(lower=0, upper=1)[10]):
    theta: real(lower=0, upper=1) <~ uniform(0, 1)
    for i in range(10):
        x[i] <~ bernoulli(theta)
```

The `@yaps.model` decorator indicates that the function following it
is a Stan program.  While being syntactically Python, it should be
semantically reinterpreted as Stan.

The argument of the function corresponds to the `data` block. The
type of the data must be declared. Here, you can see that `x` is an
array of integers between `0` and `1` (`int(lower=0, upper=1)[10]`).

Parameters are declared as variables with their type in the body of
the function. Their prior can be defined using the sampling operator
`<~`.

The body of the function corresponds to the Stan model. Python syntax
is used for the imperative constructs of the model, like the `for`
loop in the example. The operator `<~` is used to represent sampling
and `x.T[a,b]` for truncated distribution.

Other Stan blocks can be introduced using the `with` syntax of Python.
For example, the previous program could also be written as follows:
```python
@yaps.model
def coin(x: int(lower=0, upper=1)[10]):
    with parameters:
        theta: real(lower=0, upper=1)
    with model:
        theta < ~ uniform(0, 1)
        for i in range(10):
            x[i] < ~ bernoulli(theta)
```

The corresponding Stan program can be display using the `print` function:
```python
print(coin)
```

Finally, it is possible to launch the inference on the defined model applied to some data:
```python
flips = [0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
posterior = yaps.infer(coin(x=flips), iter=1000)
```
It returns `posterior`, a dictionary containing the value of the parameters:
```python
print("theta: {:.3f}".format(posterior.theta.mean()))
```

Yaps is build on top on [PyStan](http://mc-stan.org/users/interfaces/pystan). It provides a lighter
syntax to Stan programs. It allows to take advantage of Python tooling
for syntax highlighting, indentation, error reporting, ...

## Install

Yaps depends on the following packages:
- astor
- graphviz
- antlr4-python3-runtime
- pystan

To install Yaps and all its dependencies run:
```
pip install .
```


# For Yaps developers

```
pip install .[test]
nosetests tests/run_tests.py
```

Alternativaly, you can build and test the package locally:
```
make
make test
```

To test the round trip on only one file, after the install:
```
yaps-roundtrip path/to/file.stan
```

To compile a stan file to yaps:
```
stan2yaps path/to/file.stan
```


# License

Yaps is distributed under the terms of the Apache 2.0 License, see
[LICENSE.txt](LICENSE.txt)



# Contributions

Yaps is still at an early phase of development and we welcome
contributions. Contributors are expected to submit a 'Developer's
Certificate of Origin' which can be found in [DCO1.1.txt](DCO1.1.txt).

