from jedi import debug
from jedi.inference.base_value import ValueSet, NO_VALUES, ValueWrapper
from jedi.inference.gradual.base import BaseTypingValue

class TypeVarClass(ValueWrapper):
    pass

class TypeVar(BaseTypingValue):

    def __init__(self, parent_context, tree_name, var_name, unpacked_args):
        super().__init__(parent_context, tree_name)
        self._var_name = var_name
        self._constraints_lazy_values = []
        self._bound_lazy_value = None
        self._covariant_lazy_value = None
        self._contravariant_lazy_value = None
        for key, lazy_value in unpacked_args:
            if key is None:
                self._constraints_lazy_values.append(lazy_value)
            elif key == 'bound':
                self._bound_lazy_value = lazy_value
            elif key == 'covariant':
                self._covariant_lazy_value = lazy_value
            elif key == 'contravariant':
                self._contra_variant_lazy_value = lazy_value
            else:
                debug.warning('Invalid TypeVar param name %s', key)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.py__name__())

class TypeWrapper(ValueWrapper):

    def __init__(self, wrapped_value, original_value):
        super().__init__(wrapped_value)
        self._original_value = original_value