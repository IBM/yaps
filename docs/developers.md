# For Developers

To build the parser, you need to install [antlr4](http://www.antlr.org/) before installing the package.
To test your model with the Stan inference engine, you need to install [cmdstan](http://mc-stan.org/users/interfaces/cmdstan).
Then install the dependencies.

```
pip install nose astor graphviz antlr4-python3-runtime pycmdstan
make
export CMDSTAN='path/to/cmdstan-dir'
make test
```

To test the round trip on only one file, after the install:
```
yaps-roundtrip path/to/file.stan
```

## Documentation

The documentation is hosted by [ReadTheDocs](https://yaps.readthedocs.io).
To keep the README in sync with the doc:
```
make doc
```

## Distribution

To create a new distribution you need the following packages:
```
pip install setuptools wheel twine
```

Then to build the new distribution and upload it:
```
make distrib
make upload
```
Note: you need valid PyPI credentials to upload the package.
