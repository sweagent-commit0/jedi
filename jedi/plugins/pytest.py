import sys
from typing import List
from pathlib import Path
from parso.tree import search_ancestor
from jedi.inference.cache import inference_state_method_cache
from jedi.inference.imports import goto_import, load_module_from_path
from jedi.inference.filters import ParserTreeFilter
from jedi.inference.base_value import NO_VALUES, ValueSet
from jedi.inference.helpers import infer_call_of_leaf
_PYTEST_FIXTURE_MODULES = [('_pytest', 'monkeypatch'), ('_pytest', 'capture'), ('_pytest', 'logging'), ('_pytest', 'tmpdir'), ('_pytest', 'pytester')]

def _is_a_pytest_param_and_inherited(param_name):
    """
    Pytest params are either in a `test_*` function or have a pytest fixture
    with the decorator @pytest.fixture.

    This is a heuristic and will work in most cases.
    """
    pass

def _find_pytest_plugin_modules() -> List[List[str]]:
    """
    Finds pytest plugin modules hooked by setuptools entry points

    See https://docs.pytest.org/en/stable/how-to/writing_plugins.html#setuptools-entry-points
    """
    pass

class FixtureFilter(ParserTreeFilter):
    pass