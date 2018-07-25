import functools

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
    
    def infer(self, **kwargs):
        ret = pystan.stan(model_code=str(self), data=self.data, **kwargs)
        return ret

    @property
    def graph(self):
        return self.viz
    
    @property
    def ir(self):
        return self.compiled_model

    @property
    def source_map(self):
        return self.model_string

    def __str__(self):
        return str(self.model_string)

    def __repr__(self):
        return self.func
