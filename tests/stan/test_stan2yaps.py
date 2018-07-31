import yaps
from yaps.lib import *
import astor
import sys

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

do_compile(sys.argv[1])