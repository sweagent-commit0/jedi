from parso.python import tree
from jedi import debug
from jedi.inference.cache import inference_state_method_cache, CachedMetaClass
from jedi.inference import compiled
from jedi.inference import recursion
from jedi.inference import docstrings
from jedi.inference import flow_analysis
from jedi.inference.signature import TreeSignature
from jedi.inference.filters import ParserTreeFilter, FunctionExecutionFilter, AnonymousFunctionExecutionFilter
from jedi.inference.names import ValueName, AbstractNameDefinition, AnonymousParamName, ParamName, NameWrapper
from jedi.inference.base_value import ContextualizedNode, NO_VALUES, ValueSet, TreeValue, ValueWrapper
from jedi.inference.lazy_value import LazyKnownValues, LazyKnownValue, LazyTreeValue
from jedi.inference.context import ValueContext, TreeContextMixin
from jedi.inference.value import iterable
from jedi import parser_utils
from jedi.inference.parser_cache import get_yield_exprs
from jedi.inference.helpers import values_from_qualified_names
from jedi.inference.gradual.generics import TupleGenericManager

class LambdaName(AbstractNameDefinition):
    string_name = '<lambda>'
    api_type = 'function'

    def __init__(self, lambda_value):
        self._lambda_value = lambda_value
        self.parent_context = lambda_value.parent_context

class FunctionAndClassBase(TreeValue):
    pass

class FunctionMixin:
    api_type = 'function'

class FunctionValue(FunctionMixin, FunctionAndClassBase, metaclass=CachedMetaClass):
    pass

class FunctionNameInClass(NameWrapper):

    def __init__(self, class_context, name):
        super().__init__(name)
        self._class_context = class_context

class MethodValue(FunctionValue):

    def __init__(self, inference_state, class_context, *args, **kwargs):
        super().__init__(inference_state, *args, **kwargs)
        self.class_context = class_context

class BaseFunctionExecutionContext(ValueContext, TreeContextMixin):

    def infer(self):
        """
        Created to be used by inheritance.
        """
        pass

class FunctionExecutionContext(BaseFunctionExecutionContext):

    def __init__(self, function_value, arguments):
        super().__init__(function_value)
        self._arguments = arguments

class AnonymousFunctionExecution(BaseFunctionExecutionContext):
    pass

class OverloadedFunctionValue(FunctionMixin, ValueWrapper):

    def __init__(self, function, overloaded_functions):
        super().__init__(function)
        self._overloaded_functions = overloaded_functions