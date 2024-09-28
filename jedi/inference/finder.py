"""
Searching for names with given scope and name. This is very central in Jedi and
Python. The name resolution is quite complicated with descripter,
``__getattribute__``, ``__getattr__``, ``global``, etc.

If you want to understand name resolution, please read the first few chapters
in http://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/.

Flow checks
+++++++++++

Flow checks are not really mature. There's only a check for ``isinstance``.  It
would check whether a flow has the form of ``if isinstance(a, type_or_tuple)``.
Unfortunately every other thing is being ignored (e.g. a == '' would be easy to
check for -> a is a string). There's big potential in these checks.
"""
from parso.tree import search_ancestor
from parso.python.tree import Name
from jedi import settings
from jedi.inference.arguments import TreeArguments
from jedi.inference.value import iterable
from jedi.inference.base_value import NO_VALUES
from jedi.parser_utils import is_scope

def filter_name(filters, name_or_str):
    """
    Searches names that are defined in a scope (the different
    ``filters``), until a name fits.
    """
    pass

def check_flow_information(value, flow, search_name, pos):
    """ Try to find out the type of a variable just with the information that
    is given by the flows: e.g. It is also responsible for assert checks.::

        if isinstance(k, str):
            k.  # <- completion here

    ensures that `k` is a string.
    """
    pass