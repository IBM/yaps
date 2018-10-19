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

from distutils.core import setup
import os
import sys

setup(
    name='yaps',
    version='0.1dev',
    packages=['yaps', ],
    license=open('LICENSE.txt').read(),
    long_description=open('README.md').read(),
    install_requires=[
        'astor', 'graphviz', 'antlr4-python3-runtime', 'pystan<=2.17.1'
    ],
    entry_points = {
        'console_scripts': ['stan2yaps=yaps.stan2yaps:main',
                            'yaps-roundtrip=yaps.roundtrip:main'],
    }
)
