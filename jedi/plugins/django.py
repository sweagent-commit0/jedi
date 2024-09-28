"""
Module is used to infer Django model fields.
"""
from inspect import Parameter
from jedi import debug
from jedi.inference.cache import inference_state_function_cache
from jedi.inference.base_value import ValueSet, iterator_to_value_set, ValueWrapper
from jedi.inference.filters import DictFilter, AttributeOverwrite
from jedi.inference.names import NameWrapper, BaseTreeParamName
from jedi.inference.compiled.value import EmptyCompiledName
from jedi.inference.value.instance import TreeInstance
from jedi.inference.value.klass import ClassMixin
from jedi.inference.gradual.base import GenericClass
from jedi.inference.gradual.generics import TupleGenericManager
from jedi.inference.signature import AbstractSignature
mapping = {'IntegerField': (None, 'int'), 'BigIntegerField': (None, 'int'), 'PositiveIntegerField': (None, 'int'), 'SmallIntegerField': (None, 'int'), 'CharField': (None, 'str'), 'TextField': (None, 'str'), 'EmailField': (None, 'str'), 'GenericIPAddressField': (None, 'str'), 'URLField': (None, 'str'), 'FloatField': (None, 'float'), 'BinaryField': (None, 'bytes'), 'BooleanField': (None, 'bool'), 'DecimalField': ('decimal', 'Decimal'), 'TimeField': ('datetime', 'time'), 'DurationField': ('datetime', 'timedelta'), 'DateField': ('datetime', 'date'), 'DateTimeField': ('datetime', 'datetime'), 'UUIDField': ('uuid', 'UUID')}
_FILTER_LIKE_METHODS = ('create', 'filter', 'exclude', 'update', 'get', 'get_or_create', 'update_or_create')

class DjangoModelName(NameWrapper):

    def __init__(self, cls, name, is_instance):
        super().__init__(name)
        self._cls = cls
        self._is_instance = is_instance

class ManagerWrapper(ValueWrapper):
    pass

class GenericManagerWrapper(AttributeOverwrite, ClassMixin):
    pass

class FieldWrapper(ValueWrapper):
    pass

class GenericFieldWrapper(AttributeOverwrite, ClassMixin):
    pass

class DjangoModelSignature(AbstractSignature):

    def __init__(self, value, field_names):
        super().__init__(value)
        self._field_names = field_names

class DjangoParamName(BaseTreeParamName):

    def __init__(self, field_name):
        super().__init__(field_name.parent_context, field_name.tree_name)
        self._field_name = field_name

class QuerySetMethodWrapper(ValueWrapper):

    def __init__(self, method, model_cls):
        super().__init__(method)
        self._model_cls = model_cls

class QuerySetBoundMethodWrapper(ValueWrapper):

    def __init__(self, method, model_cls):
        super().__init__(method)
        self._model_cls = model_cls