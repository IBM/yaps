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
