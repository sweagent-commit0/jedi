"""
Docstrings are another source of information for functions and classes.
:mod:`jedi.inference.dynamic_params` tries to find all executions of functions,
while the docstring parsing is much easier. There are three different types of
docstrings that |jedi| understands:

- `Sphinx <http://sphinx-doc.org/markup/desc.html#info-field-lists>`_
- `Epydoc <http://epydoc.sourceforge.net/manual-fields.html>`_
- `Numpydoc <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`_

For example, the sphinx annotation ``:type foo: str`` clearly states that the
type of ``foo`` is ``str``.

As an addition to parameter searching, this module also provides return
annotations.
"""
import re
import warnings
from parso import parse, ParserSyntaxError
from jedi import debug
from jedi.inference.cache import inference_state_method_cache
from jedi.inference.base_value import iterator_to_value_set, ValueSet, NO_VALUES
from jedi.inference.lazy_value import LazyKnownValues
DOCSTRING_PARAM_PATTERNS = ['\\s*:type\\s+%s:\\s*([^\\n]+)', '\\s*:param\\s+(\\w+)\\s+%s:[^\\n]*', '\\s*@type\\s+%s:\\s*([^\\n]+)']
DOCSTRING_RETURN_PATTERNS = [re.compile('\\s*:rtype:\\s*([^\\n]+)', re.M), re.compile('\\s*@rtype:\\s*([^\\n]+)', re.M)]
REST_ROLE_PATTERN = re.compile(':[^`]+:`([^`]+)`')
_numpy_doc_string_cache = None

def _search_param_in_numpydocstr(docstr, param_str):
    """Search `docstr` (in numpydoc format) for type(-s) of `param_str`."""
    pass

def _search_return_in_numpydocstr(docstr):
    """
    Search `docstr` (in numpydoc format) for type(-s) of function returns.
    """
    pass

def _expand_typestr(type_str):
    """
    Attempts to interpret the possible types in `type_str`
    """
    pass

def _search_param_in_docstr(docstr, param_str):
    """
    Search `docstr` for type(-s) of `param_str`.

    >>> _search_param_in_docstr(':type param: int', 'param')
    ['int']
    >>> _search_param_in_docstr('@type param: int', 'param')
    ['int']
    >>> _search_param_in_docstr(
    ...   ':type param: :class:`threading.Thread`', 'param')
    ['threading.Thread']
    >>> bool(_search_param_in_docstr('no document', 'param'))
    False
    >>> _search_param_in_docstr(':param int param: some description', 'param')
    ['int']

    """
    pass

def _strip_rst_role(type_str):
    """
    Strip off the part looks like a ReST role in `type_str`.

    >>> _strip_rst_role(':class:`ClassName`')  # strip off :class:
    'ClassName'
    >>> _strip_rst_role(':py:obj:`module.Object`')  # works with domain
    'module.Object'
    >>> _strip_rst_role('ClassName')  # do nothing when not ReST role
    'ClassName'

    See also:
    http://sphinx-doc.org/domains.html#cross-referencing-python-objects

    """
    pass

def _execute_types_in_stmt(module_context, stmt):
    """
    Executing all types or general elements that we find in a statement. This
    doesn't include tuple, list and dict literals, because the stuff they
    contain is executed. (Used as type information).
    """
    pass

def _execute_array_values(inference_state, array):
    """
    Tuples indicate that there's not just one return value, but the listed
    ones.  `(str, int)` means that it returns a tuple with both types.
    """
    pass