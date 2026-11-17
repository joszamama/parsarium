# xmltodict — XML / Python

- **Pinned package:** `xmltodict` 1.0.4, [MIT license](https://pypi.org/project/xmltodict/1.0.4/).
- **Documented input API:** [`xmltodict.parse()`](https://pypi.org/project/xmltodict/) over a local binary file-like stream, with namespace processing enabled.
- **Valid control:** [`two-items.xml`](../../../../controls/xml/two-items.xml). The parser returns the `library` root namespace, two `item` children, first `id` `7`, decoded `A & B`, and decoded `π`.
- **Underlying parser family:** CPython `pyexpat` over Expat 2.10.0. The [Docker receipt](../../../../projects/xml/python/xmltodict/verification.json) records 97 `xmltodict.py` lines and 2,330 Expat lines, including 1,615 in `xmlparse.c`. The [AFL++ receipt](../../../../fuzzing/afl-native/xml/python/xmltodict/verification.json) records 3,136 source-derived tuples. This family is shared with ElementTree.

[Runnable harness](../../../../projects/xml/python/xmltodict/README.md) · [source lock](../../../../data/python/xml/source-lock.json)
