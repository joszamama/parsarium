"""Exercise CPython 3.13.1 zipfile.Path on local ZIP bytes."""
import tempfile
import adapter

def parse_data(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with tempfile.NamedTemporaryFile(suffix=".zip") as source:
        source.write(data)
        source.flush()
        return adapter.main('zipfile.Path', source.name)

def fuzz_one_input(data: bytes):
    try:
        parse_data(data)
    except (EOFError, OSError, ValueError, KeyError, IndexError):
        pass
