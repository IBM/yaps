from . import py2ir
from . import lib
from . import decorator
from . import stan2yaps
import sys

infer = lib.infer
dependent_type_var = lib.dependent_type_var
model = decorator.model


from_stan = stan2yaps.from_stan
def to_stan(code_string=None, code_file=None):
    if not (code_string or code_file) or (code_string and code_file):
        assert False, "Either string or file but not both must be provided."
    if code_string:
        ast_ = py2ir.parse_string(code_string)
    else:
        with open(code_file, 'r') as file:
            code_string = file.read()
            ast_ = py2ir.parse_string(code_string)
    return decorator.print_stan(ast_)

def roundtrip(code_file=None):
    with open(code_file, 'r') as file:
        code_string = file.read()
        print(code_string)
        print('# -------------')
        source = from_stan(code_string)
        print(source)
        print('# -------------')
        target = to_stan(code_string=source)
        print(target)

def main():
    if (len(sys.argv) <= 1):
        assert False, "File name expected"
    for i in range(1, len(sys.argv)):
        print('# -------------')
        print('#', sys.argv[i])
        print('# -------------')
        roundtrip(code_file=sys.argv[i])

