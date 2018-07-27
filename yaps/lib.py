def infer(model, *args, **kwargs):
    return model.infer(*args, **kwargs)

# Types

class dummy_full_type(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        raise TypeError("{} cannot be further constrained".format(self.name))

    def __getitem__(self, key):
        raise TypeError("{} cannot have additional dimensions".format(self.name))

    def print_dims(self, key):
        if type(key) is tuple:
            ret = ""
            first = True
            for i in key:
                if first:
                    first = False
                else:
                    ret += ", "
                ret += str(i)
            return ret
        else:
            return str(key)

class dummy_constrained_type(dummy_full_type):
    def __init__(self, name):
        dummy_full_type.__init__(self, name)

    def __getitem__(self, key):
        return dummy_full_type("{}[{}]".format(self.name, self.print_dims(key)))


class dummy_type(dummy_constrained_type):
    def __init__(self, name):
        dummy_constrained_type.__init__(self, name)

    def __call__(self, *args, **kwargs):
        return dummy_constrained_type(self.name)

class dummy_constrained_dim_type(dummy_full_type):
    def __init__(self, name, num_args):
        dummy_full_type.__init__(self, name)
        self.num_args = num_args

    def __getitem__(self, key):
        if self.num_args == 1:
            if key is tuple:
                raise TypeError("{} was given {} dimensions; {} expected".format(self.name, len(key), num_args))
            else:
                return dummy_constrained_type("{}[{}]".format(self.name, self.print_dims(key)))
        else:
            if type(key) is tuple:
                if len(key) == self.num_args:
                    return dummy_constrained_type("{}[{}]".format(self.name, self.print_dims(key)))
                else:
                    raise TypeError("{} was given {} dimensions; {} expected".format(self.name, len(key), self.num_args))
            else:
                raise TypeError("{} was given {} dimensions; {} expected".format(self.name, 1, self.num_args))

## vector/matrix types.  They must be applied to a dimension
class dummy_dim_type(dummy_constrained_dim_type):
    def __init__(self, name, num_args):
        dummy_constrained_dim_type.__init__(self, name, num_args)

    def __call__(self, *args, **kwargs):
        return dummy_constrained_dim_type(self.name, self.num_args)


int = dummy_type("int")
real = dummy_type("real")

vector = dummy_dim_type("vector", 1)
simplex = dummy_dim_type("simplex", 1)
unit_vector = dummy_dim_type("unit_vector", 1)
ordered = dummy_dim_type("ordered", 1)
positive_ordered = dummy_dim_type("positive_ordered", 1)
row_vector = dummy_dim_type("row_vector", 1)


matrix = dummy_dim_type("matrix", 2)
corr_matrix = dummy_dim_type("corr_matrix", 1)
cholesky_factor_corr = dummy_dim_type("cholesky_factor_corr", 1)
cov_matrix = dummy_dim_type("cov_matrix", 1)
cholesky_factor_cov = dummy_dim_type("cholesky_factor_cov", 1)

type_var = dummy_type
dependent_type_var = type_var("type_var")

# Blocks


class functions(object):
    def __enter__(self):
        pass

    def __exit__(self, x, y, z):
        pass


class data(object):
    def __enter__(self):
        pass

    def __exit__(self, x, y, z):
        pass


class transformed_data(object):
    def __enter__(self):
        pass

    def __exit__(self, x, y, z):
        pass


class parameters(object):
    def __enter__(self):
        pass

    def __exit__(self, x, y, z):
        pass


class transformed_parameters(object):
    def __enter__(self):
        pass

    def __exit__(self, x, y, z):
        pass


class model(object):
    def __enter__(self):
        pass

    def __exit__(self, x, y, z):
        pass


class generated_quantities(object):
    def __enter__(self):
        pass

    def __exit__(self, x, y, z):
        pass


# Distributions


def uniform(x, y):
    pass


def bernoulli(p):
    pass


def bernoulli_logit(p):
    pass


def gamma(x, y):
    pass


def normal(x, y):
    pass


# Functions

def qr_Q(x):
    return x


def qr_R(x):
    return x


def inverse(x):
    return x


def sqrt(x):
    return x
