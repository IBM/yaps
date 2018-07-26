import functools
import math
import inspect as inspect
import re as regex

from . import py2ir
import pystan

class model(object):
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)
        self.compiled_model = py2ir.parse_model(func)
        self.model_string = self.compiled_model.to_mapped_string()
        self.data = {}

    def __call__ (self, **kwargs):
        self.data.update(kwargs)
        return self
    
    def map_valueerror(self, err):
        fileName = inspect.getsourcefile(self.func)
        err = str(err)
        err = err.replace("'unknown file name'", "'" + fileName + "'")

        # 1->line, #2->col, #3->---, #4->code, #5->---
        linecolre = regex.compile("at line (\d+), column (\d+)[^-]*[^-]([-]{5,})[^-](.*)[^-]([-]{5,})", regex.MULTILINE | regex.DOTALL)

        def get_code(line, col):
            target_context_lines = 4

            py_source_lines, py_source_first_line = inspect.getsourcelines(self.func)
            context_lines = min(target_context_lines, len(py_source_lines))
            prefix_lines = math.ceil(context_lines // 2)
            start_line = max(line - prefix_lines, 0)
            overhang = max(0, start_line + context_lines - len(py_source_lines))
            start_line = max(0, start_line - overhang)

            ret = ""
            for lno in range(start_line, start_line+context_lines):
                cur_lineno = lno + py_source_first_line
                cur_line = py_source_lines[lno]
                ret += "{:>4}: {}\n".format(cur_lineno, cur_line)
                if lno == line:
                    ret += " "*(col+6)+ "^\n"
            return ret

        def mapLines(m):
            stan_line = int(m.group(1))
            stan_col = int(m.group(2))

            ir = self.source_map[stan_line-1][max(0,stan_col-2)]
            py_line = ir.lineno
            py_col = ir.col_offset

            py_source_lines, py_source_first_line = inspect.getsourcelines(self.func)
            py_code = get_code(py_line-1, py_col)

            return "at line {}, column {}\n{}\n{}\n{}\n".format(py_source_first_line+py_line-1, py_col+1, m.group(3), py_code, m.group(5))

        err = linecolre.sub(mapLines, err)

        return err
        

    def infer(self, **kwargs):
        try:
            return pystan.stan(model_code=str(self), model_name=self.func.__name__, data=self.data, **kwargs)
        except ValueError as err:
            e = ValueError(self.map_valueerror(str(err)))
            e.__traceback__ = err.__traceback__
            raise e

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

    def __str__(self):
        return str(self.model_string)

    def __repr__(self):
        return self.func
