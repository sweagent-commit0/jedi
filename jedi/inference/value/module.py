import os
from pathlib import Path
from typing import Optional
from jedi.inference.cache import inference_state_method_cache
from jedi.inference.names import AbstractNameDefinition, ModuleName
from jedi.inference.filters import GlobalNameFilter, ParserTreeFilter, DictFilter, MergedFilter
from jedi.inference import compiled
from jedi.inference.base_value import TreeValue
from jedi.inference.names import SubModuleName
from jedi.inference.helpers import values_from_qualified_names
from jedi.inference.compiled import create_simple_object
from jedi.inference.base_value import ValueSet
from jedi.inference.context import ModuleContext

class _ModuleAttributeName(AbstractNameDefinition):
    """
    For module attributes like __file__, __str__ and so on.
    """
    api_type = 'instance'

    def __init__(self, parent_module, string_name, string_value=None):
        self.parent_context = parent_module
        self.string_name = string_name
        self._string_value = string_value

class SubModuleDictMixin:

    @inference_state_method_cache()
    def sub_modules_dict(self):
        """
        Lists modules in the directory of this module (if this module is a
        package).
        """
        pass

class ModuleMixin(SubModuleDictMixin):
    _module_name_class = ModuleName

    def get_qualified_names(self):
        """
        A module doesn't have a qualified name, but it's important to note that
        it's reachable and not `None`. With this information we can add
        qualified names on top for all value children.
        """
        pass

class ModuleValue(ModuleMixin, TreeValue):
    api_type = 'module'

    def __init__(self, inference_state, module_node, code_lines, file_io=None, string_names=None, is_package=False):
        super().__init__(inference_state, parent_context=None, tree_node=module_node)
        self.file_io = file_io
        if file_io is None:
            self._path: Optional[Path] = None
        else:
            self._path = file_io.path
        self.string_names = string_names
        self.code_lines = code_lines
        self._is_package = is_package

    def py__file__(self) -> Optional[Path]:
        """
        In contrast to Python's __file__ can be None.
        """
        pass

    def py__path__(self):
        """
        In case of a package, this returns Python's __path__ attribute, which
        is a list of paths (strings).
        Returns None if the module is not a package.
        """
        pass

    def __repr__(self):
        return '<%s: %s@%s-%s is_stub=%s>' % (self.__class__.__name__, self.py__name__(), self.tree_node.start_pos[0], self.tree_node.end_pos[0], self.is_stub())