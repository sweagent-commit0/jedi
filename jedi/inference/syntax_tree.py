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
    def wrapper(*args, **kwargs):
        inference_state = args[0].inference_state
        try:
            inference_state.inferred_element_counts[func] += 1
            if inference_state.inferred_element_counts[func] > 300:
                return NO_VALUES
        except KeyError:
            inference_state.inferred_element_counts[func] = 1
        return func(*args, **kwargs)
    return wrapper

def _infer_node_if_inferred(context, element):
    """
    TODO This function is temporary: Merge with infer_node.
    """
    return context.infer_node(element)

def infer_atom(context, atom):
    """
    Basically to process ``atom`` nodes. The parser sometimes doesn't
    generate the node (because it has just one child). In that case an atom
    might be a name or a literal as well.
    """
    if atom.type == 'atom':
        first_child = atom.children[0]
        if first_child.type == 'name':
            return context.infer_node(first_child)
        elif first_child in ('(', '[', '{'):
            return context.infer_node(atom.children[1])
    elif atom.type == 'name':
        return context.infer_node(atom)
    elif atom.type in ('number', 'string', 'keyword'):
        return ValueSet([compiled.create_simple_object(context.inference_state, atom.value)])
    return NO_VALUES

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
    if seek_name:
        definition = context.tree_node.get_definition()
        if definition is not None and definition.type == 'comp_for':
            return ValueSet([iterable.CompForName(
                CompForContext(context, definition),
                seek_name,
            )])

    rhs = stmt.get_rhs()
    value_set = context.infer_node(rhs)
    if seek_name:
        return value_set.filter(lambda value: value.name.value == seek_name)

    return value_set

@iterator_to_value_set
def infer_factor(value_set, operator):
    """
    Calculates `+`, `-`, `~` and `not` prefixes.
    """
    for value in value_set:
        if operator == '-':
            if is_number(value):
                yield value.negate()
        elif operator == 'not':
            yield compiled.create_simple_object(next(iter(value_set))._inference_state, not value.py__bool__())
        elif operator == '~':
            if is_number(value):
                yield value.invert()
        else:
            yield value

@inference_state_method_cache()
@inference_state_method_cache()
def _apply_decorators(context, node):
    """
    Returns the function, that should to be executed in the end.
    This is also the places where the decorators are processed.
    """
    decorators = node.get_decorators()
    if not decorators:
        return context.infer_node(node.children[-1])
    
    values = context.infer_node(node.children[-1])
    for decorator in reversed(decorators):
        dec_values = context.infer_node(decorator.children[1])
        values = ValueSet.from_sets(
            dec_value.execute(arguments.ValuesArguments([value]))
            for dec_value in dec_values
            for value in values
        )
    return values

def check_tuple_assignments(name, value_set):
    """
    Checks if tuples are assigned.
    """
    pass

class ContextualizedSubscriptListNode(ContextualizedNode):
    def infer(self):
        return _infer_subscript_list(self.context, self.node)

def _infer_subscript_list(context, index):
    """
    Handles slices in subscript nodes.
    """
    if index == ':':
        return ValueSet([compiled.create_simple_object(context.inference_state, slice(None, None, None))])
    elif index.type == 'subscript':
        start = index.children[0] if index.children[0] != ':' else None
        stop = index.children[2] if len(index.children) > 2 and index.children[2] != ':' else None
        step = index.children[4] if len(index.children) > 4 else None
        
        start_values = context.infer_node(start) if start else ValueSet([compiled.create_simple_object(context.inference_state, None)])
        stop_values = context.infer_node(stop) if stop else ValueSet([compiled.create_simple_object(context.inference_state, None)])
        step_values = context.infer_node(step) if step else ValueSet([compiled.create_simple_object(context.inference_state, None)])
        
        return ValueSet([
            compiled.create_simple_object(context.inference_state, slice(s.obj, e.obj, t.obj))
            for s in start_values
            for e in stop_values
            for t in step_values
        ])
    else:
        return context.infer_node(index)
