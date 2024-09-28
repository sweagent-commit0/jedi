import re
from textwrap import dedent
from inspect import Parameter
from parso.python.token import PythonTokenTypes
from parso.python import tree
from parso.tree import search_ancestor, Leaf
from parso import split_lines
from jedi import debug
from jedi import settings
from jedi.api import classes
from jedi.api import helpers
from jedi.api import keywords
from jedi.api.strings import complete_dict
from jedi.api.file_name import complete_file_name
from jedi.inference import imports
from jedi.inference.base_value import ValueSet
from jedi.inference.helpers import infer_call_of_leaf, parse_dotted_names
from jedi.inference.context import get_global_filters
from jedi.inference.value import TreeInstance
from jedi.inference.docstring_utils import DocstringModule
from jedi.inference.names import ParamNameWrapper, SubModuleName
from jedi.inference.gradual.conversion import convert_values, convert_names
from jedi.parser_utils import cut_value_at_position
from jedi.plugins import plugin_manager

class ParamNameWithEquals(ParamNameWrapper):
    pass

def get_user_context(module_context, position):
    """
    Returns the scope in which the user resides. This includes flows.
    """
    pass

class Completion:

    def __init__(self, inference_state, module_context, code_lines, position, signatures_callback, fuzzy=False):
        self._inference_state = inference_state
        self._module_context = module_context
        self._module_node = module_context.tree_node
        self._code_lines = code_lines
        self._like_name = helpers.get_on_completion_name(self._module_node, code_lines, position)
        self._original_position = position
        self._signatures_callback = signatures_callback
        self._fuzzy = fuzzy

    def _complete_python(self, leaf):
        """
        Analyzes the current context of a completion and decides what to
        return.

        Technically this works by generating a parser stack and analysing the
        current stack for possible grammar nodes.

        Possible enhancements:
        - global/nonlocal search global
        - yield from / raise from <- could be only exceptions/generators
        - In args: */**: no completion
        - In params (also lambda): no completion before =
        """
        pass

    def _complete_inherited(self, is_function=True):
        """
        Autocomplete inherited methods when overriding in child class.
        """
        pass

    def _complete_in_string(self, start_leaf, string):
        """
        To make it possible for people to have completions in doctests or
        generally in "Python" code in docstrings, we use the following
        heuristic:

        - Having an indented block of code
        - Having some doctest code that starts with `>>>`
        - Having backticks that doesn't have whitespace inside it
        """
        pass
_string_start = re.compile('^\\w*(\\\'{3}|"{3}|\\\'|")')

def _complete_getattr(user_context, instance):
    """
    A heuristic to make completion for proxy objects work. This is not
    intended to work in all cases. It works exactly in this case:

        def __getattr__(self, name):
            ...
            return getattr(any_object, name)

    It is important that the return contains getattr directly, otherwise it
    won't work anymore. It's really just a stupid heuristic. It will not
    work if you write e.g. `return (getatr(o, name))`, because of the
    additional parentheses. It will also not work if you move the getattr
    to some other place that is not the return statement itself.

    It is intentional that it doesn't work in all cases. Generally it's
    really hard to do even this case (as you can see below). Most people
    will write it like this anyway and the other ones, well they are just
    out of luck I guess :) ~dave.
    """
    pass