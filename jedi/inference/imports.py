"""
:mod:`jedi.inference.imports` is here to resolve import statements and return
the modules/classes/functions/whatever, which they stand for. However there's
not any actual importing done. This module is about finding modules in the
filesystem. This can be quite tricky sometimes, because Python imports are not
always that simple.

This module also supports import autocompletion, which means to complete
statements like ``from datetim`` (cursor at the end would return ``datetime``).
"""
import os
from pathlib import Path
from parso.python import tree
from parso.tree import search_ancestor
from jedi import debug
from jedi import settings
from jedi.file_io import FolderIO
from jedi.parser_utils import get_cached_code_lines
from jedi.inference import sys_path
from jedi.inference import helpers
from jedi.inference import compiled
from jedi.inference import analysis
from jedi.inference.utils import unite
from jedi.inference.cache import inference_state_method_cache
from jedi.inference.names import ImportName, SubModuleName
from jedi.inference.base_value import ValueSet, NO_VALUES
from jedi.inference.gradual.typeshed import import_module_decorator, create_stub_module, parse_stub_module
from jedi.inference.compiled.subprocess.functions import ImplicitNSInfo
from jedi.plugins import plugin_manager

class ModuleCache:

    def __init__(self):
        self._name_cache = {}

def _level_to_base_import_path(project_path, directory, level):
    """
    In case the level is outside of the currently known package (something like
    import .....foo), we can still try our best to help the user for
    completions.
    """
    pass

class Importer:

    def __init__(self, inference_state, import_path, module_context, level=0):
        """
        An implementation similar to ``__import__``. Use `follow`
        to actually follow the imports.

        *level* specifies whether to use absolute or relative imports. 0 (the
        default) means only perform absolute imports. Positive values for level
        indicate the number of parent directories to search relative to the
        directory of the module calling ``__import__()`` (see PEP 328 for the
        details).

        :param import_path: List of namespaces (strings or Names).
        """
        debug.speed('import %s %s' % (import_path, module_context))
        self._inference_state = inference_state
        self.level = level
        self._module_context = module_context
        self._fixed_sys_path = None
        self._infer_possible = True
        if level:
            base = module_context.get_value().py__package__()
            if level <= len(base):
                base = tuple(base)
                if level > 1:
                    base = base[:-level + 1]
                import_path = base + tuple(import_path)
            else:
                path = module_context.py__file__()
                project_path = self._inference_state.project.path
                import_path = list(import_path)
                if path is None:
                    directory = project_path
                else:
                    directory = os.path.dirname(path)
                base_import_path, base_directory = _level_to_base_import_path(project_path, directory, level)
                if base_directory is None:
                    self._infer_possible = False
                else:
                    self._fixed_sys_path = [base_directory]
                if base_import_path is None:
                    if import_path:
                        _add_error(module_context, import_path[0], message='Attempted relative import beyond top-level package.')
                else:
                    import_path = base_import_path + import_path
        self.import_path = import_path

    @property
    def _str_import_path(self):
        """Returns the import path as pure strings instead of `Name`."""
        pass

    def _get_module_names(self, search_path=None, in_module=None):
        """
        Get the names of all modules in the search_path. This means file names
        and not names defined in the files.
        """
        pass

    def completion_names(self, inference_state, only_modules=False):
        """
        :param only_modules: Indicates wheter it's possible to import a
            definition that is not defined in a module.
        """
        pass

@plugin_manager.decorate()
@import_module_decorator
def import_module(inference_state, import_names, parent_module_value, sys_path):
    """
    This method is very similar to importlib's `_gcd_import`.
    """
    pass

def load_module_from_path(inference_state, file_io, import_names=None, is_package=None):
    """
    This should pretty much only be used for get_modules_containing_name. It's
    here to ensure that a random path is still properly loaded into the Jedi
    module structure.
    """
    pass

def iter_module_names(inference_state, module_context, search_path, module_cls=ImportName, add_builtin_modules=True):
    """
    Get the names of all modules in the search_path. This means file names
    and not names defined in the files.
    """
    pass