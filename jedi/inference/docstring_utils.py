from jedi.inference.value import ModuleValue
from jedi.inference.context import ModuleContext

class DocstringModule(ModuleValue):

    def __init__(self, in_module_context, **kwargs):
        super().__init__(**kwargs)
        self._in_module_context = in_module_context

class DocstringModuleContext(ModuleContext):

    def __init__(self, module_value, in_module_context):
        super().__init__(module_value)
        self._in_module_context = in_module_context