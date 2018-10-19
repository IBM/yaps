# Copyright 2018 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup
import os
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='yaps',
    version='0.1.1',
    author="Guillaume Baudart, Martin Hirzel, Kiran Kate, Louis Mandel, Avraham Shinnar",
    description="A surface language for programming Stan models using python syntax",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ibm.github.io/yaps/",
    packages=['yaps', ],
    license='Apache License 2.0',
    install_requires=[
        'astor', 'graphviz', 'antlr4-python3-runtime', 'pystan<=2.17.1'
    ],
    entry_points = {
        'console_scripts': ['stan2yaps=yaps.stan2yaps:main',
                            'yaps-roundtrip=yaps.roundtrip:main'],
    }
)