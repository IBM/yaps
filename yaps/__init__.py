from . import py2ir
from . import lib
from . import decorator

parse_model = py2ir.parse_model
model = decorator.model
infer = lib.infer
dependent_type_var = lib.dependent_type_var
