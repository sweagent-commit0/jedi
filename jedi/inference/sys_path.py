import os
import re
from pathlib import Path
from importlib.machinery import all_suffixes
from jedi.inference.cache import inference_state_method_cache
from jedi.inference.base_value import ContextualizedNode
from jedi.inference.helpers import is_string, get_str_or_none
from jedi.parser_utils import get_cached_code_lines
from jedi.file_io import FileIO
from jedi import settings
from jedi import debug
_BUILDOUT_PATH_INSERTION_LIMIT = 10

def _paths_from_assignment(module_context, expr_stmt):
    """
    Extracts the assigned strings from an assignment that looks as follows::

        sys.path[0:0] = ['module/path', 'another/module/path']

    This function is in general pretty tolerant (and therefore 'buggy').
    However, it's not a big issue usually to add more paths to Jedi's sys_path,
    because it will only affect Jedi in very random situations and by adding
    more paths than necessary, it usually benefits the general user.
    """
    pass

def _paths_from_list_modifications(module_context, trailer1, trailer2):
    """ extract the path from either "sys.path.append" or "sys.path.insert" """
    pass

@inference_state_method_cache(default=[])
def check_sys_path_modifications(module_context):
    """
    Detect sys.path modifications within module.
    """
    pass

def _get_buildout_script_paths(search_path: Path):
    """
    if there is a 'buildout.cfg' file in one of the parent directories of the
    given module it will return a list of all files in the buildout bin
    directory that look like python files.

    :param search_path: absolute path to the module.
    """
    pass

def transform_path_to_dotted(sys_path, module_path):
    """
    Returns the dotted path inside a sys.path as a list of names. e.g.

    >>> transform_path_to_dotted([str(Path("/foo").absolute())], Path('/foo/bar/baz.py').absolute())
    (('bar', 'baz'), False)

    Returns (None, False) if the path doesn't really resolve to anything.
    The second return part is if it is a package.
    """
    pass