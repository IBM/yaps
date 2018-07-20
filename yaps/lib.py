# Types


def dummy_type(**kwargs):
    class DummyList:
        def __getitem__(self, key):
            return None
    return DummyList()


int = dummy_type
real = dummy_type


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
