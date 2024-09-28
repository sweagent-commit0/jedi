"""
Decorators are not really values, however we need some wrappers to improve
docstrings and other things around decorators.
"""
from jedi.inference.base_value import ValueWrapper, ValueSet

class Decoratee(ValueWrapper):

    def __init__(self, wrapped_value, original_value):
        super().__init__(wrapped_value)
        self._original_value = original_value