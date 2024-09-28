"""
Contains all classes and functions to deal with lists, dicts, generators and
iterators in general.
"""
from jedi.inference import compiled
from jedi.inference import analysis
from jedi.inference.lazy_value import LazyKnownValue, LazyKnownValues, LazyTreeValue
from jedi.inference.helpers import get_int_or_none, is_string, reraise_getitem_errors, SimpleGetItemNotFound
from jedi.inference.utils import safe_property, to_list
from jedi.inference.cache import inference_state_method_cache
from jedi.inference.filters import LazyAttributeOverwrite, publish_method
from jedi.inference.base_value import ValueSet, Value, NO_VALUES, ContextualizedNode, iterate_values, sentinel, LazyValueWrapper
from jedi.parser_utils import get_sync_comp_fors
from jedi.inference.context import CompForContext
from jedi.inference.value.dynamic_arrays import check_array_additions

class IterableMixin:
    get_safe_value = Value.get_safe_value

class GeneratorBase(LazyAttributeOverwrite, IterableMixin):
    array_type = None

class Generator(GeneratorBase):
    """Handling of `yield` functions."""

    def __init__(self, inference_state, func_execution_context):
        super().__init__(inference_state)
        self._func_execution_context = func_execution_context

    def __repr__(self):
        return '<%s of %s>' % (type(self).__name__, self._func_execution_context)

class ComprehensionMixin:

    def __repr__(self):
        return '<%s of %s>' % (type(self).__name__, self._sync_comp_for_node)

class _DictMixin:
    pass

class Sequence(LazyAttributeOverwrite, IterableMixin):
    api_type = 'instance'

class _BaseComprehension(ComprehensionMixin):

    def __init__(self, inference_state, defining_context, sync_comp_for_node, entry_node):
        assert sync_comp_for_node.type == 'sync_comp_for'
        super().__init__(inference_state)
        self._defining_context = defining_context
        self._sync_comp_for_node = sync_comp_for_node
        self._entry_node = entry_node

class ListComprehension(_BaseComprehension, Sequence):
    array_type = 'list'

class SetComprehension(_BaseComprehension, Sequence):
    array_type = 'set'

class GeneratorComprehension(_BaseComprehension, GeneratorBase):
    pass

class _DictKeyMixin:
    pass

class DictComprehension(ComprehensionMixin, Sequence, _DictKeyMixin):
    array_type = 'dict'

    def __init__(self, inference_state, defining_context, sync_comp_for_node, key_node, value_node):
        assert sync_comp_for_node.type == 'sync_comp_for'
        super().__init__(inference_state)
        self._defining_context = defining_context
        self._sync_comp_for_node = sync_comp_for_node
        self._entry_node = key_node
        self._value_node = value_node

class SequenceLiteralValue(Sequence):
    _TUPLE_LIKE = ('testlist_star_expr', 'testlist', 'subscriptlist')
    mapping = {'(': 'tuple', '[': 'list', '{': 'set'}

    def __init__(self, inference_state, defining_context, atom):
        super().__init__(inference_state)
        self.atom = atom
        self._defining_context = defining_context
        if self.atom.type in self._TUPLE_LIKE:
            self.array_type = 'tuple'
        else:
            self.array_type = SequenceLiteralValue.mapping[atom.children[0]]
            'The builtin name of the array (list, set, tuple or dict).'

    def py__simple_getitem__(self, index):
        """Here the index is an int/str. Raises IndexError/KeyError."""
        pass

    def py__iter__(self, contextualized_node=None):
        """
        While values returns the possible values for any array field, this
        function returns the value for a certain index.
        """
        pass

    def __repr__(self):
        return '<%s of %s>' % (self.__class__.__name__, self.atom)

class DictLiteralValue(_DictMixin, SequenceLiteralValue, _DictKeyMixin):
    array_type = 'dict'

    def __init__(self, inference_state, defining_context, atom):
        Sequence.__init__(self, inference_state)
        self._defining_context = defining_context
        self.atom = atom

    def py__simple_getitem__(self, index):
        """Here the index is an int/str. Raises IndexError/KeyError."""
        pass

    def py__iter__(self, contextualized_node=None):
        """
        While values returns the possible values for any array field, this
        function returns the value for a certain index.
        """
        pass

    def exact_key_items(self):
        """
        Returns a generator of tuples like dict.items(), where the key is
        resolved (as a string) and the values are still lazy values.
        """
        pass

class _FakeSequence(Sequence):

    def __init__(self, inference_state, lazy_value_list):
        """
        type should be one of "tuple", "list"
        """
        super().__init__(inference_state)
        self._lazy_value_list = lazy_value_list

    def __repr__(self):
        return '<%s of %s>' % (type(self).__name__, self._lazy_value_list)

class FakeTuple(_FakeSequence):
    array_type = 'tuple'

class FakeList(_FakeSequence):
    array_type = 'tuple'

class FakeDict(_DictMixin, Sequence, _DictKeyMixin):
    array_type = 'dict'

    def __init__(self, inference_state, dct):
        super().__init__(inference_state)
        self._dct = dct

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self._dct)

class MergedArray(Sequence):

    def __init__(self, inference_state, arrays):
        super().__init__(inference_state)
        self.array_type = arrays[-1].array_type
        self._arrays = arrays

def unpack_tuple_to_dict(context, types, exprlist):
    """
    Unpacking tuple assignments in for statements and expr_stmts.
    """
    pass

class Slice(LazyValueWrapper):

    def __init__(self, python_context, start, stop, step):
        self.inference_state = python_context.inference_state
        self._context = python_context
        self._start = start
        self._stop = stop
        self._step = step

    def get_safe_value(self, default=sentinel):
        """
        Imitate CompiledValue.obj behavior and return a ``builtin.slice()``
        object.
        """
        pass