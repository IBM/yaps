# Copyright 2018 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import math
import inspect as inspect
import re as regex
import sys
import pystan
from . import py2ir

class FitModel(object):
    def __init__(self, fit_model):
        self.__model = fit_model

    def __getattr__(self, key):
        return self.__model.extract()[key]

    def __getitem__(self, key):
        return self.__model.extract()[key]

    def __dir__(self):
        return self.__model.extract()

    def __str__(self):
        ret = ""
        for k, v in self.__model.extract().items():
            print("{}: {}".format(k, v))
        return ret

class model_with_args(object):
    def __init__(self, model, data):
        self.model = model
        self.stored_data = data

    def __call__(self, **kwargs):
        d = self.stored_data.copy()
        d.update(kwargs)
        return model_with_args(self.model, d)

    def map_valueerror(self, err):
        fileName = inspect.getsourcefile(self.model.func)
        err = str(err)
        err = err.replace("'unknown file name'", "'" + fileName + "'")

        # 1->line, #2->col, #3->---, #4->code, #5->---
        linecolre = regex.compile(
            "at line (\d+), column (\d+)[^-]*[^-]([-]{5,})[^-](.*)[^-]([-]{5,})", regex.MULTILINE | regex.DOTALL)

        def get_code(line, col):
            target_context_lines = 4

            py_source_lines, py_source_first_line = inspect.getsourcelines(
                self.model.func)
            context_lines = min(target_context_lines, len(py_source_lines))
            prefix_lines = math.ceil(context_lines // 2)
            start_line = max(line - prefix_lines, 0)
            overhang = max(0, start_line + context_lines -
                           len(py_source_lines))
            start_line = max(0, start_line - overhang)

            ret = ""
            for lno in range(start_line, start_line+context_lines):
                cur_lineno = lno + py_source_first_line
                cur_line = py_source_lines[lno]
                ret += "{:>4}: {}".format(cur_lineno, cur_line)
                if lno == line:
                    ret += " "*(col+6) + "^\n"
            return ret

        def mapLines(m):
            stan_line = int(m.group(1))
            stan_col = int(m.group(2))

            ir = self.source_map[stan_line-1][max(0, stan_col-2)]
            py_line = ir.lineno
            py_col = ir.col_offset

            py_source_lines, py_source_first_line = inspect.getsourcelines(
                self.model.func)
            py_code = get_code(py_line-1, py_col)
            if not py_code.endswith("\n"):
                py_code += "\n"
            return "at line {}, column {}\n{}\n{}{}\n".format(py_source_first_line+py_line-1, py_col+1, m.group(3), py_code, m.group(5))

        err = linecolre.sub(mapLines, err)

        return err

    def infer(self, **kwargs):
        try:
            return FitModel(pystan.stan(model_code=self.model.stan_code, model_name=self.model.func.__name__, data=self.stored_data, **kwargs))
        except ValueError as err:
            e = ValueError(self.map_valueerror(str(err)))
            e.__traceback__ = err.__traceback__
            raise e

    @property
    def graph(self):
        return self.model.graph

    @property
    def ir(self):
        return self.model.ir

    @property
    def source_map(self):
        return self.model.source_map

    @property
    def stan_code(self):
        return self.model.stan_code

    @property
    def data(self):
        return self.stored_data

    def __str__(self):
        return "stan:\n{}\ndata:\n{}".format(self.model, self.data)

    def __repr__(self):
        return self.model.__repr__


class model(object):
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)
        self.compiled_model = py2ir.parse_function(func)
        self.model_string = self.compiled_model.to_mapped_string()
        self.viz = self.compiled_model.viz()

    def __call__(self, **kwargs):
        if kwargs:
            return model_with_args(self, kwargs)
        else:
            return self

    def infer(self, **kwargs):
        return model_with_args(self, {}).infer(**kwargs)

    @property
    def graph(self):
        return self.viz

    @property
    def ir(self):
        return self.compiled_model

    @property
    def source_map(self):
        return self.model_string

    @property
    def stan_code(self):
        return str(self)

    @property
    def data(self):
        return {}

    def __str__(self):
        return str(self.model_string)

    def __repr__(self):
        return self.func

def print_stan(ir):
    return str(ir.to_mapped_string())

def to_stan(code_string=None, code_file=None):
    if not (code_string or code_file) or (code_string and code_file):
        assert False, "Either string or file but not both must be provided."
    if code_string:
        ast_ = py2ir.parse_string(code_string)
    else:
        with open(code_file, 'r') as file:
            code_string = file.read()
            ast_ = py2ir.parse_string(code_string)
    return print_stan(ast_)