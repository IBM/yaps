from . import py2ir
from . import lib
from . import decorator
from . import stan2yaps

parse_model = py2ir.parse_model
to_stan = decorator.print_stan
model = decorator.model
infer = lib.infer
dependent_type_var = lib.dependent_type_var
from_stan = stan2yaps.from_stan
from_string = py2ir.parse_string
ast_from_stan = stan2yaps.do_compile
