# Inference

Communication with the Stan inference engine is based on [PyStan](https://pystan.readthedocs.io/en/latest/).
When a model is defined, the name of the model is linked to the compiled Stan code.

## PyStan API
The first option is to use the PyStan API to call the inference engine with `str(model)` for the model code.

For example:
```python
from yaps.lib import int, real, uniform, bernoulli
import yaps as yaps
import pystan

@yaps.model
def coin(x: int(lower=0, upper=1)[10]):
    theta: real(lower=0, upper=1) is uniform(0, 1)
    for i in range(10):
        x[i] is bernoulli(theta)

coin_dat = {'x': [1,0,1,0,1,0,0,0,0,1]}
fit = pystan.stan(model_code=str(coin), data=coin_dat, iter=1000)
theta_mean = fit.extract(permuted=True)['theta'].mean()
print("mean of theta: {:.3f}".format(theta_mean))
```

## Yaps infer

Alternatively, Yaps provides an `yaps.infer` function that is a wrapper for `pystan.stan`.
Compared to `pystan.stan` data are passed to the model as keyword parameters.
After the inference `yaps.infer` returns an object with fields for parameters.
For instance the second part of the previous example can be rewritten:

```python
flips = [0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
posterior = yaps.infer(coin(x=flips), iter=1000)
theta_mean = posterior.theta.mean()
print("mean of theta: {:.3f}".format(theta_mean))
```
