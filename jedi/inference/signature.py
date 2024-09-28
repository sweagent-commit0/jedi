from inspect import Parameter
from jedi.cache import memoize_method
from jedi import debug
from jedi import parser_utils

class _SignatureMixin:
    pass

class AbstractSignature(_SignatureMixin):

    def __init__(self, value, is_bound=False):
        self.value = value
        self.is_bound = is_bound

    def __repr__(self):
        if self.value is self._function_value:
            return '<%s: %s>' % (self.__class__.__name__, self.value)
        return '<%s: %s, %s>' % (self.__class__.__name__, self.value, self._function_value)

class TreeSignature(AbstractSignature):

    def __init__(self, value, function_value=None, is_bound=False):
        super().__init__(value, is_bound)
        self._function_value = function_value or value

class BuiltinSignature(AbstractSignature):

    def __init__(self, value, return_string, function_value=None, is_bound=False):
        super().__init__(value, is_bound)
        self._return_string = return_string
        self.__function_value = function_value

class SignatureWrapper(_SignatureMixin):

    def __init__(self, wrapped_signature):
        self._wrapped_signature = wrapped_signature

    def __getattr__(self, name):
        return getattr(self._wrapped_signature, name)