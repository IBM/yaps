from distutils.core import setup

setup(
    name='Yaps',
    version='0.1dev',
    packages=['yaps', ],
    license=open('LICENSE.txt').read(),
    long_description=open('README.md').read(),
    install_requires=[
        'astor', 'graphviz', 'antlr4-python3-runtime', 'pystan'
    ]
)
