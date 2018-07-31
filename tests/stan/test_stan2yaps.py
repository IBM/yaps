import yaps
from yaps.lib import *
import astor
import sys
from pathlib import Path

def do_compile(path):
    with open(path, 'r') as fin:
        print(fin.read())
    print('--------------------------------')
    source = yaps.from_stan(code_file=path)
    print(source)
    print('--------------------------------')
    ast_ = yaps.from_string(source)
    yaps.print_stan(ast_)
    print('--------------------------------')




def run_test(dir):
    pathlist = Path(dir).glob('**/*.stan')
    for p in pathlist:
        path = str(p)
        print(path)
        source = yaps.from_stan(code_file=path)
        ast_ = yaps.from_string(source)

        # because path is object not string
        # path_in_str = str(path)

        # print(path_in_str)



do_compile(sys.argv[1])
# run_test('tests/stan')