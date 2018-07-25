def infer(model, *args, **kwargs):
    return model.infer(*args, **kwargs)

# Types

class dummy_type(object):
    def __getitem__(self, key):
        return None

    def __init__(self):
        pass

    def __call__ (self, *args, **kwargs):
        return dummy_type()


int = dummy_type()
real = dummy_type()


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


def gamma(x, y):
    pass


def normal(x, y):
    pass
