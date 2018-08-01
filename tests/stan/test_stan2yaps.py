import yaps
from yaps.lib import *
import astor
import sys
from pathlib import Path

def roundtrip(path):
    with open(path, 'r') as fin:
        print(fin.read())
    print('--------------------------------')
    source = yaps.from_stan(code_file=path)
    print(source)
    print('--------------------------------')
    ast_ = yaps.from_string(source)
    print(yaps.to_stan(ast_))
    print('--------------------------------')


def run_test(dir):
    pathlist = Path(dir).glob('**/*.stan')
    nb_test = 0
    nb_success = 0
    for p in pathlist:
        path = str(p)
        nb_test += 1
        try:
            source = yaps.from_stan(code_file=path)
            ast_ = yaps.from_string(source)
            stan = yaps.to_stan(ast_)
            nb_success += 1
        except (AttributeError, SyntaxError, TypeError, AssertionError) as err:
             print("ASSERT\t", path, err)

    print("-------------------------")
    print("{}% of success ({}/{} stan examples)".format(nb_success/nb_test * 100, nb_success, nb_test))

run_test('tests/stan')