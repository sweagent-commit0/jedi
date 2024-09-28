from typing import Dict, Tuple, Callable
CacheValues = Tuple[str, str, str]
CacheValuesCallback = Callable[[], CacheValues]
_cache: Dict[str, Dict[str, CacheValues]] = {}
get_type = _create_get_from_cache(0)
get_docstring_signature = _create_get_from_cache(1)
get_docstring = _create_get_from_cache(2)