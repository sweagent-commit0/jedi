import pydoc
from contextlib import suppress
from typing import Dict, Optional
from jedi.inference.names import AbstractArbitraryName
try:
    from pydoc_data import topics
    pydoc_topics: Optional[Dict[str, str]] = topics.topics
except ImportError:
    pydoc_topics = None

class KeywordName(AbstractArbitraryName):
    api_type = 'keyword'

def imitate_pydoc(string):
    """
    It's not possible to get the pydoc's without starting the annoying pager
    stuff.
    """
    pass