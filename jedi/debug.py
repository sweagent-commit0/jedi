import os
import time
from contextlib import contextmanager
from typing import Callable, Optional
_inited = False

def _lazy_colorama_init():
    """
    Lazily init colorama if necessary, not to screw up stdout if debugging is
    not enabled.

    This version of the function does nothing.
    """
    pass
try:
    if os.name == 'nt':
        raise ImportError
    else:
        from colorama import Fore, init
        from colorama import initialise

        def _lazy_colorama_init():
            """
            Lazily init colorama if necessary, not to screw up stdout is
            debug not enabled.

            This version of the function does init colorama.
            """
            pass
except ImportError:

    class Fore:
        RED = ''
        GREEN = ''
        YELLOW = ''
        MAGENTA = ''
        RESET = ''
        BLUE = ''
NOTICE = object()
WARNING = object()
SPEED = object()
enable_speed = False
enable_warning = False
enable_notice = False
debug_function: Optional[Callable[[str, str], None]] = None
_debug_indent = 0
_start_time = time.time()

def increase_indent(func):
    """Decorator for makin """
    pass

def dbg(message, *args, color='GREEN'):
    """ Looks at the stack, to see if a debug message should be printed. """
    pass

def print_to_stdout(color, str_out):
    """
    The default debug function that prints to standard out.

    :param str color: A string that is an attribute of ``colorama.Fore``.
    """
    pass