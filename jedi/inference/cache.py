"""
- the popular ``_memoize_default`` works like a typical memoize and returns the
  default otherwise.
- ``CachedMetaClass`` uses ``_memoize_default`` to do the same with classes.
"""
from functools import wraps
from jedi import debug
_NO_DEFAULT = object()
_RECURSION_SENTINEL = object()

def _memoize_default(default=_NO_DEFAULT, inference_state_is_first_arg=False, second_arg_is_inference_state=False):
    """ This is a typical memoization decorator, BUT there is one difference:
    To prevent recursion it sets defaults.

    Preventing recursion is in this case the much bigger use than speed. I
    don't think, that there is a big speed difference, but there are many cases
    where recursion could happen (think about a = b; b = a).
    """
    pass

class CachedMetaClass(type):
    """
    This is basically almost the same than the decorator above, it just caches
    class initializations. Either you do it this way or with decorators, but
    with decorators you lose class access (isinstance, etc).
    """

    @inference_state_as_method_param_cache()
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

def inference_state_method_generator_cache():
    """
    This is a special memoizer. It memoizes generators and also checks for
    recursion errors and returns no further iterator elemends in that case.
    """
    pass