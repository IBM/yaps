# For Developers

To build the parser, you need to install [antlr](http://www.antlr.org/) before installing the package.
You will also need to install the nose package to run the tests.
For instance using homebrew:
```
brew install antlr
pip install nose astor graphviz antlr4-python3-runtime pystan
make
make test
```
Or equivalently on Ubuntu:
```
apt install antlr4
pip install nose astor graphviz antlr4-python3-runtime pystan
make
make test
```

To test the round trip on only one file, after the install:
```
yaps-roundtrip path/to/file.stan
```

## Documentation

The documentation is written with Sphinx, using a Markdown parser, and the readthedoc theme.
You thus need to install the following packages:
```
pip install sphinx sphinx_rtd_theme recommonmark
```

Then to generate the documentation:
```
make doc
```
The version number used in the documentation corresponds to the last installed version.
You might want to run `pip install .` before generating the doc.

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
