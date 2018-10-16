from . import py2ir
from . import lib
from . import decorator
from . import stan2yaps
import sys

infer = lib.infer
dependent_type_var = lib.dependent_type_var
model = decorator.model

from_stan = stan2yaps.from_stan
to_stan = decorator.to_stan

