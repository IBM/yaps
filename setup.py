from distutils.core import setup
import os
import sys

os.system("antlr4 -Dlanguage=Python3 yaps/stan.g4")

setup(
    name='yaps',
    version='0.1dev',
    packages=['yaps', ],
    license=open('LICENSE.txt').read(),
    long_description=open('README.md').read(),
    extras_require={ 'test': ['nose'] },
    install_requires=[
        'astor', 'graphviz', 'antlr4-python3-runtime', 'pystan'
    ],
    entry_points = {
        'console_scripts': ['stan2yaps=yaps.stan2yaps:main',
                            'yaps-roundtrip=yaps.decorator:main'],
    }
)
