import sys
import os
import inspect
import importlib
from pathlib import Path
from zipfile import ZipFile
from zipimport import zipimporter, ZipImportError
from importlib.machinery import all_suffixes
from jedi.inference.compiled import access
from jedi import debug
from jedi import parser_utils
from jedi.file_io import KnownContentFileIO, ZipFileIO

def get_module_info(inference_state, sys_path=None, full_name=None, **kwargs):
    """
    Returns Tuple[Union[NamespaceInfo, FileIO, None], Optional[bool]]
    """
    pass

def _test_raise_error(inference_state, exception_type):
    """
    Raise an error to simulate certain problems for unit tests.
    """
    pass

def _test_print(inference_state, stderr=None, stdout=None):
    """
    Force some prints in the subprocesses. This exists for unit tests.
    """
    pass

def _get_init_path(directory_path):
    """
    The __init__ file can be searched in a directory. If found return it, else
    None.
    """
    pass

def _find_module(string, path=None, full_name=None, is_global_search=True):
    """
    Provides information about a module.

    This function isolates the differences in importing libraries introduced with
    python 3.3 on; it gets a module name and optionally a path. It will return a
    tuple containin an open file for the module (if not builtin), the filename
    or the name of the module if it is a builtin one and a boolean indicating
    if the module is contained in a package.
    """
    pass

def _get_source(loader, fullname):
    """
    This method is here as a replacement for SourceLoader.get_source. That
    method returns unicode, but we prefer bytes.
    """
    pass

class ImplicitNSInfo:
    """Stores information returned from an implicit namespace spec"""

    def __init__(self, name, paths):
        self.name = name
        self.paths = paths