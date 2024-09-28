from jedi.inference.base_value import ValueSet, NO_VALUES
from jedi.common import monkeypatch

class AbstractLazyValue:

    def __init__(self, data, min=1, max=1):
        self.data = data
        self.min = min
        self.max = max

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.data)

class LazyKnownValue(AbstractLazyValue):
    """data is a Value."""

class LazyKnownValues(AbstractLazyValue):
    """data is a ValueSet."""

class LazyUnknownValue(AbstractLazyValue):

    def __init__(self, min=1, max=1):
        super().__init__(None, min, max)

class LazyTreeValue(AbstractLazyValue):

    def __init__(self, context, node, min=1, max=1):
        super().__init__(node, min, max)
        self.context = context
        self._predefined_names = dict(context.predefined_names)

class MergedLazyValues(AbstractLazyValue):
    """data is a list of lazy values."""