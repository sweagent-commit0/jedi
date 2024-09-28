"""
This module is responsible for inferring *args and **kwargs for signatures.

This means for example in this case::

    def foo(a, b, c): ...

    def bar(*args):
        return foo(1, *args)

The signature here for bar should be `bar(b, c)` instead of bar(*args).
"""
from inspect import Parameter
from parso import tree
from jedi.inference.utils import to_list
from jedi.inference.names import ParamNameWrapper
from jedi.inference.helpers import is_big_annoying_library

class ParamNameFixedKind(ParamNameWrapper):

    def __init__(self, param_name, new_kind):
        super().__init__(param_name)
        self._new_kind = new_kind