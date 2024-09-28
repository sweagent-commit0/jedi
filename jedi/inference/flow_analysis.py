from typing import Dict, Optional
from jedi.parser_utils import get_flow_branch_keyword, is_scope, get_parent_scope
from jedi.inference.recursion import execution_allowed
from jedi.inference.helpers import is_big_annoying_library

class Status:
    lookup_table: Dict[Optional[bool], 'Status'] = {}

    def __init__(self, value: Optional[bool], name: str) -> None:
        self._value = value
        self._name = name
        Status.lookup_table[value] = self

    def __and__(self, other):
        if UNSURE in (self, other):
            return UNSURE
        else:
            return REACHABLE if self._value and other._value else UNREACHABLE

    def __repr__(self):
        return '<%s: %s>' % (type(self).__name__, self._name)
REACHABLE = Status(True, 'reachable')
UNREACHABLE = Status(False, 'unreachable')
UNSURE = Status(None, 'unsure')