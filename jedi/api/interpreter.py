"""
TODO Some parts of this module are still not well documented.
"""
from jedi.inference import compiled
from jedi.inference.base_value import ValueSet
from jedi.inference.filters import ParserTreeFilter, MergedFilter
from jedi.inference.names import TreeNameDefinition
from jedi.inference.compiled import mixed
from jedi.inference.compiled.access import create_access_path
from jedi.inference.context import ModuleContext

class NamespaceObject:

    def __init__(self, dct):
        self.__dict__ = dct

class MixedTreeName(TreeNameDefinition):

    def infer(self):
        """
        In IPython notebook it is typical that some parts of the code that is
        provided was already executed. In that case if something is not properly
        inferred, it should still infer from the variables it already knows.
        """
        pass

class MixedParserTreeFilter(ParserTreeFilter):
    name_class = MixedTreeName

class MixedModuleContext(ModuleContext):

    def __init__(self, tree_module_value, namespaces):
        super().__init__(tree_module_value)
        self.mixed_values = [self._get_mixed_object(_create(self.inference_state, NamespaceObject(n))) for n in namespaces]