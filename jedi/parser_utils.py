import re
import textwrap
from ast import literal_eval
from inspect import cleandoc
from weakref import WeakKeyDictionary
from parso.python import tree
from parso.cache import parser_cache
from parso import split_lines
_EXECUTE_NODES = {'funcdef', 'classdef', 'import_from', 'import_name', 'test', 'or_test', 'and_test', 'not_test', 'comparison', 'expr', 'xor_expr', 'and_expr', 'shift_expr', 'arith_expr', 'atom_expr', 'term', 'factor', 'power', 'atom'}
_FLOW_KEYWORDS = ('try', 'except', 'finally', 'else', 'if', 'elif', 'with', 'for', 'while')

def get_executable_nodes(node, last_added=False):
    """
    For static analysis.
    """
    pass

def for_stmt_defines_one_name(for_stmt):
    """
    Returns True if only one name is returned: ``for x in y``.
    Returns False if the for loop is more complicated: ``for x, z in y``.

    :returns: bool
    """
    pass

def clean_scope_docstring(scope_node):
    """ Returns a cleaned version of the docstring token. """
    pass

def get_signature(funcdef, width=72, call_string=None, omit_first_param=False, omit_return_annotation=False):
    """
    Generate a string signature of a function.

    :param width: Fold lines if a line is longer than this value.
    :type width: int
    :arg func_name: Override function name when given.
    :type func_name: str

    :rtype: str
    """
    pass

def move(node, line_offset):
    """
    Move the `Node` start_pos.
    """
    pass

def get_following_comment_same_line(node):
    """
    returns (as string) any comment that appears on the same line,
    after the node, including the #
    """
    pass

def get_parent_scope(node, include_flows=False):
    """
    Returns the underlying scope.
    """
    pass
get_cached_parent_scope = _get_parent_scope_cache(get_parent_scope)

def get_cached_code_lines(grammar, path):
    """
    Basically access the cached code lines in parso. This is not the nicest way
    to do this, but we avoid splitting all the lines again.
    """
    pass

def get_parso_cache_node(grammar, path):
    """
    This is of course not public. But as long as I control parso, this
    shouldn't be a problem. ~ Dave

    The reason for this is mostly caching. This is obviously also a sign of a
    broken caching architecture.
    """
    pass

def cut_value_at_position(leaf, position):
    """
    Cuts of the value of the leaf at position
    """
    pass

def expr_is_dotted(node):
    """
    Checks if a path looks like `name` or `name.foo.bar` and not `name()`.
    """
    pass
function_is_staticmethod = _function_is_x_method('staticmethod')
function_is_classmethod = _function_is_x_method('classmethod')
function_is_property = _function_is_x_method('property', 'cached_property')