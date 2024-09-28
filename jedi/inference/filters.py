"""
Filters are objects that you can use to filter names in different scopes. They
are needed for name resolution.
"""
from abc import abstractmethod
from typing import List, MutableMapping, Type
import weakref
from parso.tree import search_ancestor
from parso.python.tree import Name, UsedNamesMapping
from jedi.inference import flow_analysis
from jedi.inference.base_value import ValueSet, ValueWrapper, LazyValueWrapper
from jedi.parser_utils import get_cached_parent_scope, get_parso_cache_node
from jedi.inference.utils import to_list
from jedi.inference.names import TreeNameDefinition, ParamName, AnonymousParamName, AbstractNameDefinition, NameWrapper
_definition_name_cache: MutableMapping[UsedNamesMapping, List[Name]]
_definition_name_cache = weakref.WeakKeyDictionary()

class AbstractFilter:
    _until_position = None

class FilterWrapper:
    name_wrapper_class: Type[NameWrapper]

    def __init__(self, wrapped_filter):
        self._wrapped_filter = wrapped_filter

class _AbstractUsedNamesFilter(AbstractFilter):
    name_class = TreeNameDefinition

    def __init__(self, parent_context, node_context=None):
        if node_context is None:
            node_context = parent_context
        self._node_context = node_context
        self._parser_scope = node_context.tree_node
        module_context = node_context.get_root_context()
        path = module_context.py__file__()
        if path is None:
            self._parso_cache_node = None
        else:
            self._parso_cache_node = get_parso_cache_node(module_context.inference_state.latest_grammar if module_context.is_stub() else module_context.inference_state.grammar, path)
        self._used_names = module_context.tree_node.get_used_names()
        self.parent_context = parent_context

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.parent_context)

class ParserTreeFilter(_AbstractUsedNamesFilter):

    def __init__(self, parent_context, node_context=None, until_position=None, origin_scope=None):
        """
        node_context is an option to specify a second value for use cases
        like the class mro where the parent class of a new name would be the
        value, but for some type inference it's important to have a local
        value of the other classes.
        """
        super().__init__(parent_context, node_context)
        self._origin_scope = origin_scope
        self._until_position = until_position

class _FunctionExecutionFilter(ParserTreeFilter):

    def __init__(self, parent_context, function_value, until_position, origin_scope):
        super().__init__(parent_context, until_position=until_position, origin_scope=origin_scope)
        self._function_value = function_value

class FunctionExecutionFilter(_FunctionExecutionFilter):

    def __init__(self, *args, arguments, **kwargs):
        super().__init__(*args, **kwargs)
        self._arguments = arguments

class AnonymousFunctionExecutionFilter(_FunctionExecutionFilter):
    pass

class GlobalNameFilter(_AbstractUsedNamesFilter):
    pass

class DictFilter(AbstractFilter):

    def __init__(self, dct):
        self._dct = dct

    def __repr__(self):
        keys = ', '.join(self._dct.keys())
        return '<%s: for {%s}>' % (self.__class__.__name__, keys)

class MergedFilter:

    def __init__(self, *filters):
        self._filters = filters

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join((str(f) for f in self._filters)))

class _BuiltinMappedMethod(ValueWrapper):
    """``Generator.__next__`` ``dict.values`` methods and so on."""
    api_type = 'function'

    def __init__(self, value, method, builtin_func):
        super().__init__(builtin_func)
        self._value = value
        self._method = method

class SpecialMethodFilter(DictFilter):
    """
    A filter for methods that are defined in this module on the corresponding
    classes like Generator (for __next__, etc).
    """

    class SpecialMethodName(AbstractNameDefinition):
        api_type = 'function'

        def __init__(self, parent_context, string_name, callable_, builtin_value):
            self.parent_context = parent_context
            self.string_name = string_name
            self._callable = callable_
            self._builtin_value = builtin_value

    def __init__(self, value, dct, builtin_value):
        super().__init__(dct)
        self.value = value
        self._builtin_value = builtin_value
        '\n        This value is what will be used to introspect the name, where as the\n        other value will be used to execute the function.\n\n        We distinguish, because we have to.\n        '

class _OverwriteMeta(type):

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        base_dct = {}
        for base_cls in reversed(cls.__bases__):
            try:
                base_dct.update(base_cls.overwritten_methods)
            except AttributeError:
                pass
        for func in cls.__dict__.values():
            try:
                base_dct.update(func.registered_overwritten_methods)
            except AttributeError:
                pass
        cls.overwritten_methods = base_dct

class _AttributeOverwriteMixin:
    pass

class LazyAttributeOverwrite(_AttributeOverwriteMixin, LazyValueWrapper, metaclass=_OverwriteMeta):

    def __init__(self, inference_state):
        self.inference_state = inference_state

class AttributeOverwrite(_AttributeOverwriteMixin, ValueWrapper, metaclass=_OverwriteMeta):
    pass