from contextlib import contextmanager

@contextmanager
def monkeypatch(obj, attribute_name, new_value):
    """
    Like pytest's monkeypatch, but as a value manager.
    """
    pass

def indent_block(text, indention='    '):
    """This function indents a text block with a default of four spaces."""
    pass