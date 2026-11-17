# ElementTree — XML / Python standard library

- **Pinned runtime:** CPython 3.14.4 in the container, with `ElementTree.py` checked by SHA-256 and Expat 2.10.0 built from pinned source.
- **Official input API:** [`xml.etree.ElementTree.parse()`](https://docs.python.org/3.14/library/xml.etree.elementtree.html) over a local binary file-like stream; `getroot()` exposes the parsed tree.
- **Valid control:** [`two-items.xml`](../../../../controls/xml/two-items.xml), producing the root namespace, two child elements, first attribute `id=7`, and decoded text `A & B` and `π`.
- **Parser family:** CPython ElementTree over Expat. The [Docker receipt](../../../../projects/xml/python/stdlib_elementtree/verification.json) records 16 `ElementTree.py` lines and 2,280 Expat lines, including 1,565 in `xmlparse.c`. The [AFL++ receipt](../../../../fuzzing/afl-native/xml/python/stdlib_elementtree/verification.json) records 3,086 source-derived tuples. This standard API is listed separately from PyPI package popularity.

[Runnable harness](../../../../projects/xml/python/stdlib_elementtree/README.md) · [source lock](../../../../data/python/xml/source-lock.json)
