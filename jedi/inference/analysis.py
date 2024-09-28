"""
Module for statical analysis.
"""
from parso.python import tree
from jedi import debug
from jedi.inference.helpers import is_string
CODES = {'attribute-error': (1, AttributeError, 'Potential AttributeError.'), 'name-error': (2, NameError, 'Potential NameError.'), 'import-error': (3, ImportError, 'Potential ImportError.'), 'type-error-too-many-arguments': (4, TypeError, None), 'type-error-too-few-arguments': (5, TypeError, None), 'type-error-keyword-argument': (6, TypeError, None), 'type-error-multiple-values': (7, TypeError, None), 'type-error-star-star': (8, TypeError, None), 'type-error-star': (9, TypeError, None), 'type-error-operation': (10, TypeError, None), 'type-error-not-iterable': (11, TypeError, None), 'type-error-isinstance': (12, TypeError, None), 'type-error-not-subscriptable': (13, TypeError, None), 'value-error-too-many-values': (14, ValueError, None), 'value-error-too-few-values': (15, ValueError, None)}

class Error:

    def __init__(self, name, module_path, start_pos, message=None):
        self.path = module_path
        self._start_pos = start_pos
        self.name = name
        if message is None:
            message = CODES[self.name][2]
        self.message = message

    def __str__(self):
        return '%s:%s:%s: %s %s' % (self.path, self.line, self.column, self.code, self.message)

    def __eq__(self, other):
        return self.path == other.path and self.name == other.name and (self._start_pos == other._start_pos)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.path, self._start_pos, self.name))

    def __repr__(self):
        return '<%s %s: %s@%s,%s>' % (self.__class__.__name__, self.name, self.path, self._start_pos[0], self._start_pos[1])

class Warning(Error):
    pass

def _check_for_setattr(instance):
    """
    Check if there's any setattr method inside an instance. If so, return True.
    """
    pass

def _check_for_exception_catch(node_context, jedi_name, exception, payload=None):
    """
    Checks if a jedi object (e.g. `Statement`) sits inside a try/catch and
    doesn't count as an error (if equal to `exception`).
    Also checks `hasattr` for AttributeErrors and uses the `payload` to compare
    it.
    Returns True if the exception was catched.
    """
    pass