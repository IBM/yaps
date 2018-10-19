from . import stan2yaps
from . import decorator
import sys

def roundtrip(code_file=None):
    with open(code_file, 'r') as file:
        code_string = file.read()
        print(code_string)
        print('# -------------')
        source = stan2yaps.from_stan(code_string)
        print(source)
        print('# -------------')
        target = decorator.to_stan(code_string=source)
        print(target)

def main():
    if (len(sys.argv) <= 1):
        assert False, "File name expected"
    for i in range(1, len(sys.argv)):
        print('# -------------')
        print('#', sys.argv[i])
        print('# -------------')
        roundtrip(code_file=sys.argv[i])