# Inference

By default, communication with the Stan inference engine is based on [PyCmdStan](https://pycmdstan.readthedocs.io/en/latest/).
A constrained model can be defined by passing concrete values for the data.
This constrained model is linked to a PyCmdStan model.
It is thus possible to invoke the pycmdstan methods `sample`, `run`, `optimize`, or `variational` to launch the inference.
After the inference, the result is stored in the `posterior` attribute of the constrained model as an object with one field for each learned parameter.

For example:
```
@yaps.model
def coin(x: int(lower=0, upper=1)[10]):
    theta: real(lower=0, upper=1) is uniform(0, 1)
    for i in range(2, 11):
        x[i] is bernoulli(theta)


flips = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 1])

constrained_coin = coin(x=flips)
constrained_coin.sample(data=constrained_coin.data)
theta_mean = constrained_coin.posterior.theta.mean()
print("mean of theta: {:.3f}".format(theta_mean))
```

Errors detected by the Stan compiler and runtime are mapped to the original yaps code.

Note that this interface takes full advantage of the features offered by PyCmdStan.
In particular, models are cached and only recompiled when a change is detected even if the rest of the python script has changed.

## PyStan Wrapper

Yaps also offer a limited wrapper for the [PyStan](https://pystan.readthedocs.io/en/latest/) interface.
For instance, the inference part of the previous example can be rewritten:

```
fit = yaps.apply(pystan.stan, constrained_coin)
theta_mean = fit.extract()['theta'].mean()
print("mean of theta: {:.3f}".format(theta_mean))
```

The wrapper is used to map the errors back to the original yaps code.


## Direct API use

Finally it is possible to use yaps only as a compiler and rely on the existing API for PyCmdStan or PyStan.
For every decorated yaps model `model`, the string `str(model)` contains the compiled Stan code.

Using PyCmdStan the previous example becomes:
```
coin_dat = {'x': np.array([1,0,1,0,1,0,0,0,0,1])}
coin_model = pycmdstan.Model(code = str(coin))
fit = coin_model.sample(data = coin_dat)
theta_mean = fit.csv['theta'].mean()
print("mean of theta: {:.3f}".format(theta_mean))
```

And using PyStan
```
coin_dat = {'x': np.array([1,0,1,0,1,0,0,0,0,1])}
fit = pystan.stan(model_code=str(coin), data=coin_dat)
theta_mean = fit.extract(permuted=True)['theta'].mean()
print("mean of theta: {:.3f}".format(theta_mean))
```