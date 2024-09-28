import re
from itertools import zip_longest
from parso.python import tree
from jedi import debug
from jedi.inference.utils import PushBackIterator
from jedi.inference import analysis
from jedi.inference.lazy_value import LazyKnownValue, LazyKnownValues, LazyTreeValue, get_merged_lazy_value
from jedi.inference.names import ParamName, TreeNameDefinition, AnonymousParamName
from jedi.inference.base_value import NO_VALUES, ValueSet, ContextualizedNode
from jedi.inference.value import iterable
from jedi.inference.cache import inference_state_as_method_param_cache

def try_iter_content(types, depth=0):
    """Helper method for static analysis."""
    pass

class ParamIssue(Exception):
    pass

def repack_with_argument_clinic(clinic_string):
    """
    Transforms a function or method with arguments to the signature that is
    given as an argument clinic notation.

    Argument clinic is part of CPython and used for all the functions that are
    implemented in C (Python 3.7):

        str.split.__text_signature__
        # Results in: '($self, /, sep=None, maxsplit=-1)'
    """
    pass

def iterate_argument_clinic(inference_state, arguments, clinic_string):
    """Uses a list with argument clinic information (see PEP 436)."""
    pass

class _AbstractArgumentsMixin:
    pass

class AbstractArguments(_AbstractArgumentsMixin):
    context = None
    argument_node = None
    trailer = None

class TreeArguments(AbstractArguments):

    def __init__(self, inference_state, context, argument_node, trailer=None):
        """
        :param argument_node: May be an argument_node or a list of nodes.
        """
        self.argument_node = argument_node
        self.context = context
        self._inference_state = inference_state
        self.trailer = trailer

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.argument_node)

class ValuesArguments(AbstractArguments):

    def __init__(self, values_list):
        self._values_list = values_list

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self._values_list)

class TreeArgumentsWrapper(_AbstractArgumentsMixin):

    def __init__(self, arguments):
        self._wrapped_arguments = arguments

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self._wrapped_arguments)