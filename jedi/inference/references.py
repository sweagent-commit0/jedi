import os
import re
from parso import python_bytes_to_unicode
from jedi.debug import dbg
from jedi.file_io import KnownContentFileIO, FolderIO
from jedi.inference.names import SubModuleName
from jedi.inference.imports import load_module_from_path
from jedi.inference.filters import ParserTreeFilter
from jedi.inference.gradual.conversion import convert_names
_IGNORE_FOLDERS = ('.tox', '.venv', '.mypy_cache', 'venv', '__pycache__')
_OPENED_FILE_LIMIT = 2000
"\nStats from a 2016 Lenovo Notebook running Linux:\nWith os.walk, it takes about 10s to scan 11'000 files (without filesystem\ncaching). Once cached it only takes 5s. So it is expected that reading all\nthose files might take a few seconds, but not a lot more.\n"
_PARSED_FILE_LIMIT = 30
'\nFor now we keep the amount of parsed files really low, since parsing might take\neasily 100ms for bigger files.\n'

def get_module_contexts_containing_name(inference_state, module_contexts, name, limit_reduction=1):
    """
    Search a name in the directories of modules.

    :param limit_reduction: Divides the limits on opening/parsing files by this
        factor.
    """
    pass