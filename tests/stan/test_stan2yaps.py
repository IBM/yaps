import yaps
import astor

def do_compile(path):
    x = yaps.from_stan(code_file=path)
    print(x)

do_compile('tests/stan/coin.stan')