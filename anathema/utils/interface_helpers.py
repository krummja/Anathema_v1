from functools import partial, wraps
import inspect
from ecstremity import Component


# The / parameter denotes that all preceding arguments are positional
# It is basically the inverse of *
def foo(a, /, *args, **kwargs):
    return a(*args, **kwargs)


def to_interface(method=None, *args, **kwargs):
    method_name = method.__name__
    print(vars(method))

    def wrapper(self):
        method(*args, **kwargs)
    return wrapper

    # if method.__self__:
    #     classes = [method.__self__.__class__]
    # else:
    #     classes = []
    # while classes:
    #     c = classes.pop()
    #
    #     if method_name in c.__dict__:
    #         if isinstance(c, Component):
    #             ui_client = c.client
    #             ui_client.register(f'{c.__name__}_{method_name}')
    #         else:
    #             raise AttributeError("No interface client to route to.")
    #
    # def wrapper(self):
    #     """Sends an iterable of (name, event) tuples to the client interface."""
    #     data = func(*args, **kwargs)
    #     if data is not None:
    #         ui_client.update(data)
    #
    # return wrapper
