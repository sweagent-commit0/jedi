import copy
import sys
import re
import os
from itertools import chain
from contextlib import contextmanager
from parso.python import tree

def deep_ast_copy(obj):
    """
    Much, much faster than copy.deepcopy, but just for parser tree nodes.
    """
    pass

def infer_call_of_leaf(context, leaf, cut_own_trailer=False):
    """
    Creates a "call" node that consist of all ``trailer`` and ``power``
    objects.  E.g. if you call it with ``append``::

        list([]).append(3) or None

    You would get a node with the content ``list([]).append`` back.

    This generates a copy of the original ast node.

    If you're using the leaf, e.g. the bracket `)` it will return ``list([])``.

    We use this function for two purposes. Given an expression ``bar.foo``,
    we may want to
      - infer the type of ``foo`` to offer completions after foo
      - infer the type of ``bar`` to be able to jump to the definition of foo
    The option ``cut_own_trailer`` must be set to true for the second purpose.
    """
    pass

class SimpleGetItemNotFound(Exception):
    pass