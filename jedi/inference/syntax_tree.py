"""
Functions inferring the syntax tree.
"""
import copy
import itertools
from parso.python import tree
from jedi import debug
from jedi import parser_utils
from jedi.inference.base_value import ValueSet, NO_VALUES, ContextualizedNode, iterator_to_value_set, iterate_values
from jedi.inference.lazy_value import LazyTreeValue
from jedi.inference import compiled
from jedi.inference import recursion
from jedi.inference import analysis
from jedi.inference import imports
from jedi.inference import arguments
from jedi.inference.value import ClassValue, FunctionValue
from jedi.inference.value import iterable
from jedi.inference.value.dynamic_arrays import ListModification, DictModification
from jedi.inference.value import TreeInstance
from jedi.inference.helpers import is_string, is_literal, is_number, get_names_of_node, is_big_annoying_library
from jedi.inference.compiled.access import COMPARISON_OPERATORS
from jedi.inference.cache import inference_state_method_cache
from jedi.inference.gradual.stub_value import VersionInfo
from jedi.inference.gradual import annotation
from jedi.inference.names import TreeNameDefinition
from jedi.inference.context import CompForContext
from jedi.inference.value.decorator import Decoratee
from jedi.plugins import plugin_manager
operator_to_magic_method = {'+': '__add__', '-': '__sub__', '*': '__mul__', '@': '__matmul__', '/': '__truediv__', '//': '__floordiv__', '%': '__mod__', '**': '__pow__', '<<': '__lshift__', '>>': '__rshift__', '&': '__and__', '|': '__or__', '^': '__xor__'}
reverse_operator_to_magic_method = {k: '__r' + v[2:] for k, v in operator_to_magic_method.items()}

def _limit_value_infers(func):
    """
    This is for now the way how we limit type inference going wild. There are
    other ways to ensure recursion limits as well. This is mostly necessary
    because of instance (self) access that can be quite tricky to limit.

    I'm still not sure this is the way to go, but it looks okay for now and we
    can still go anther way in the future. Tests are there. ~ dave
    """
    pass

def _infer_node_if_inferred(context, element):
    """
    TODO This function is temporary: Merge with infer_node.
    """
    pass

def infer_atom(context, atom):
    """
    Basically to process ``atom`` nodes. The parser sometimes doesn't
    generate the node (because it has just one child). In that case an atom
    might be a name or a literal as well.
    """
    pass

@debug.increase_indent
def _infer_expr_stmt(context, stmt, seek_name=None):
    """
    The starting point of the completion. A statement always owns a call
    list, which are the calls, that a statement does. In case multiple
    names are defined in the statement, `seek_name` returns the result for
    this name.

    expr_stmt: testlist_star_expr (annassign | augassign (yield_expr|testlist) |
                     ('=' (yield_expr|testlist_star_expr))*)
    annassign: ':' test ['=' test]
    augassign: ('+=' | '-=' | '*=' | '@=' | '/=' | '%=' | '&=' | '|=' | '^=' |
                '<<=' | '>>=' | '**=' | '//=')

    :param stmt: A `tree.ExprStmt`.
    """
    pass

@iterator_to_value_set
def infer_factor(value_set, operator):
    """
    Calculates `+`, `-`, `~` and `not` prefixes.
    """
    pass

@inference_state_method_cache()
def _apply_decorators(context, node):
    """
    Returns the function, that should to be executed in the end.
    This is also the places where the decorators are processed.
    """
    pass

def check_tuple_assignments(name, value_set):
    """
    Checks if tuples are assigned.
    """
    pass

class ContextualizedSubscriptListNode(ContextualizedNode):
    pass

def _infer_subscript_list(context, index):
    """
    Handles slices in subscript nodes.
    """
    pass