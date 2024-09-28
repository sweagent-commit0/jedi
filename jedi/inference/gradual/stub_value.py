from jedi.inference.base_value import ValueWrapper
from jedi.inference.value.module import ModuleValue
from jedi.inference.filters import ParserTreeFilter
from jedi.inference.names import StubName, StubModuleName
from jedi.inference.gradual.typing import TypingModuleFilterWrapper
from jedi.inference.context import ModuleContext

class StubModuleValue(ModuleValue):
    _module_name_class = StubModuleName

    def __init__(self, non_stub_value_set, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.non_stub_value_set = non_stub_value_set

    def sub_modules_dict(self):
        """
        We have to overwrite this, because it's possible to have stubs that
        don't have code for all the child modules. At the time of writing this
        there are for example no stubs for `json.tool`.
        """
        pass

class StubModuleContext(ModuleContext):
    pass

class TypingModuleWrapper(StubModuleValue):
    pass

class TypingModuleContext(ModuleContext):
    pass

class StubFilter(ParserTreeFilter):
    name_class = StubName

class VersionInfo(ValueWrapper):
    pass