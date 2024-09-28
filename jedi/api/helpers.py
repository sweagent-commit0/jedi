"""
Helpers for the API
"""
import re
from collections import namedtuple
from textwrap import dedent
from itertools import chain
from functools import wraps
from inspect import Parameter
from parso.python.parser import Parser
from parso.python import tree
from jedi.inference.base_value import NO_VALUES
from jedi.inference.syntax_tree import infer_atom
from jedi.inference.helpers import infer_call_of_leaf
from jedi.inference.compiled import get_string_value_set
from jedi.cache import signature_time_cache, memoize_method
from jedi.parser_utils import get_parent_scope
CompletionParts = namedtuple('CompletionParts', ['path', 'has_dot', 'name'])

class OnErrorLeaf(Exception):
    pass

def get_stack_at_position(grammar, code_lines, leaf, pos):
    """
    Returns the possible node names (e.g. import_from, xor_test or yield_stmt).
    """
    pass

class CallDetails:

    def __init__(self, bracket_leaf, children, position):
        self.bracket_leaf = bracket_leaf
        self._children = children
        self._position = position

def _get_index_and_key(nodes, position):
    """
    Returns the amount of commas and the keyword argument string.
    """
    pass

@signature_time_cache('call_signatures_validity')
def cache_signatures(inference_state, context, bracket_leaf, code_lines, user_pos):
    """This function calculates the cache key."""
    pass

def get_module_names(module, all_scopes, definitions=True, references=False):
    """
    Returns a dictionary with name parts as keys and their call paths as
    values.
    """
    pass