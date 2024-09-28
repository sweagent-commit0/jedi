"""
A module to deal with stuff like `list.append` and `set.add`.

Array modifications
*******************

If the content of an array (``set``/``list``) is requested somewhere, the
current module will be checked for appearances of ``arr.append``,
``arr.insert``, etc.  If the ``arr`` name points to an actual array, the
content will be added

This can be really cpu intensive, as you can imagine. Because |jedi| has to
follow **every** ``append`` and check whether it's the right array. However this
works pretty good, because in *slow* cases, the recursion detector and other
settings will stop this process.

It is important to note that:

1. Array modifications work only in the current module.
2. Jedi only checks Array additions; ``list.pop``, etc are ignored.
"""
from jedi import debug
from jedi import settings
from jedi.inference import recursion
from jedi.inference.base_value import ValueSet, NO_VALUES, HelperValueMixin, ValueWrapper
from jedi.inference.lazy_value import LazyKnownValues
from jedi.inference.helpers import infer_call_of_leaf
from jedi.inference.cache import inference_state_method_cache
_sentinel = object()

def check_array_additions(context, sequence):
    """ Just a mapper function for the internal _internal_check_array_additions """
    pass

@inference_state_method_cache(default=NO_VALUES)
@debug.increase_indent
def _internal_check_array_additions(context, sequence):
    """
    Checks if a `Array` has "add" (append, insert, extend) statements:

    >>> a = [""]
    >>> a.append(1)
    """
    pass

def get_dynamic_array_instance(instance, arguments):
    """Used for set() and list() instances."""
    pass

class _DynamicArrayAdditions(HelperValueMixin):
    """
    Used for the usage of set() and list().
    This is definitely a hack, but a good one :-)
    It makes it possible to use set/list conversions.

    This is not a proper context, because it doesn't have to be. It's not used
    in the wild, it's just used within typeshed as an argument to `__init__`
    for set/list and never used in any other place.
    """

    def __init__(self, instance, arguments):
        self._instance = instance
        self._arguments = arguments

class _Modification(ValueWrapper):

    def __init__(self, wrapped_value, assigned_values, contextualized_key):
        super().__init__(wrapped_value)
        self._assigned_values = assigned_values
        self._contextualized_key = contextualized_key

class DictModification(_Modification):
    pass

class ListModification(_Modification):
    pass