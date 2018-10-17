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

from pathlib import Path
import yaps
import pystan
import sys

def check_roundtrip(path):
    with open(path, 'r') as fin:
        code = fin.read()
        try:
            pystan.stanc(model_code=code)
            try:
                source = yaps.from_stan(code_file=path)
            except (AttributeError, SyntaxError, TypeError, AssertionError, ValueError):
                assert False, 'Error: Stan2Yaps'
            try:
                stan = yaps.to_stan(source)
            except (AttributeError, SyntaxError, TypeError, AssertionError, ValueError):
                assert False, 'Error: Yaps2Stan'
            try:
                pystan.stanc(model_code=stan)
            except (AttributeError, SyntaxError, TypeError, AssertionError, ValueError):
                assert False, 'Error: Invalid Compiled Stan code'
        except (ValueError, RuntimeError):
            assert True, 'Error: Invalid Original Stan code'

def test_stan():
    pathlist = Path('tests/stan').glob('*.stan')
    for p in pathlist:
        path = str(p)
        yield check_roundtrip, path
