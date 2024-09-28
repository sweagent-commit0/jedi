"""
This module is here for string completions. This means mostly stuff where
strings are returned, like `foo = dict(bar=3); foo["ba` would complete to
`"bar"]`.

It however does the same for numbers. The difference between string completions
and other completions is mostly that this module doesn't return defined
names in a module, but pretty much an arbitrary string.
"""
import re
from jedi.inference.names import AbstractArbitraryName
from jedi.inference.helpers import infer_call_of_leaf
from jedi.api.classes import Completion
from jedi.parser_utils import cut_value_at_position
_sentinel = object()

class StringName(AbstractArbitraryName):
    api_type = 'string'
    is_value_name = False