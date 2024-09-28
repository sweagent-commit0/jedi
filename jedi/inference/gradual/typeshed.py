import os
import re
from functools import wraps
from collections import namedtuple
from typing import Dict, Mapping, Tuple
from pathlib import Path
from jedi import settings
from jedi.file_io import FileIO
from jedi.parser_utils import get_cached_code_lines
from jedi.inference.base_value import ValueSet, NO_VALUES
from jedi.inference.gradual.stub_value import TypingModuleWrapper, StubModuleValue
from jedi.inference.value import ModuleValue
_jedi_path = Path(__file__).parent.parent.parent
TYPESHED_PATH = _jedi_path.joinpath('third_party', 'typeshed')
DJANGO_INIT_PATH = _jedi_path.joinpath('third_party', 'django-stubs', 'django-stubs', '__init__.pyi')
_IMPORT_MAP = dict(_collections='collections', _socket='socket')
PathInfo = namedtuple('PathInfo', 'path is_third_party')

def _create_stub_map(directory_path_info):
    """
    Create a mapping of an importable name in Python to a stub file.
    """
    pass
_version_cache: Dict[Tuple[int, int], Mapping[str, PathInfo]] = {}

def _cache_stub_file_map(version_info):
    """
    Returns a map of an importable name in Python to a stub file.
    """
    pass

def _try_to_load_stub(inference_state, import_names, python_value_set, parent_module_value, sys_path):
    """
    Trying to load a stub for a set of import_names.

    This is modelled to work like "PEP 561 -- Distributing and Packaging Type
    Information", see https://www.python.org/dev/peps/pep-0561.
    """
    pass