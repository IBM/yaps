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
import pycmdstan
import sys
import tempfile
import os


def check_roundtrip(path):
    with open(path, 'r') as fin:
        code = fin.read()
        print(code)
    try:
        pycmdstan.model.preprocess_model(path, overwrite=True)
        try:
            source = yaps.from_stan(code_file=path)
        except (AttributeError, SyntaxError, TypeError, AssertionError, ValueError):
            assert False, 'Error: Stan2Yaps'
        try:
            stan = yaps.to_stan(source)
        except (AttributeError, SyntaxError, TypeError, AssertionError, ValueError):
            assert False, 'Error: Yaps2Stan'
        try:
            stan_file = tempfile.NamedTemporaryFile(suffix='.stan')
            stan_file.write(bytes(stan, 'utf-8'))
            stan_file.flush()
            pycmdstan.model.preprocess_model(stan_file.name)
            stan_file.close()
        except (AttributeError, SyntaxError, TypeError, AssertionError, ValueError):
            assert False, 'Error: Invalid Compiled Stan code'
    except (ValueError, RuntimeError):
        assert True, 'Error: Invalid Original Stan code'


def test_stan():
    pathlist = Path('tests/stan').glob('*.stan')
    for p in pathlist:
        path = str(p)
        print(path)
        yield check_roundtrip, path
