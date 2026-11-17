"""Print an exact, type-tagged JSON tree for one local file.

Modes: ``json5-bytes``, ``json5-str`` and ``json5-stream`` call json5.loads on bytes,
json5.loads on decoded text and json5.load on a local binary stream; ``stdlib`` is the
independent CPython json oracle and must run where json5 is absent.
"""
from io import BytesIO
import json
import json.decoder
import json.scanner
import sys
from pathlib import Path


def tagged(value):
    # bool before int: bool is an int subclass.
    if isinstance(value, bool):
        return ['bool', value]
    if value is None:
        return ['null']
    if isinstance(value, int):
        return ['int', str(value)]
    if isinstance(value, float):
        return ['float', value.hex()]
    if isinstance(value, str):
        return ['string', value]
    if isinstance(value, list):
        return ['array', [tagged(item) for item in value]]
    if isinstance(value, dict):
        return ['object', [[key, tagged(item)] for key, item in value.items()]]
    raise TypeError(type(value).__name__)


def main() -> None:
    mode, path = sys.argv[1], Path(sys.argv[2])
    data = path.read_bytes()
    report = {'mode': mode}
    if mode == 'stdlib':
        try:
            import json5  # noqa: F401
        except ModuleNotFoundError:
            pass
        else:
            raise SystemExit('stdlib oracle must not see json5')
        pairs_seen = []
        value = json.loads(data, object_pairs_hook=lambda pairs: pairs_seen.append(len(pairs)) or dict(pairs))
        # A shorter dict than its pair list would mean a duplicate key in the control.
        report.update({'python': sys.version.split()[0], 'json_c_scanner': json.scanner.c_make_scanner is not None,
                       'json_c_scanstring': json.decoder.c_scanstring is not None,
                       'object_pairs': sum(pairs_seen)})
    elif mode in ('json5-bytes', 'json5-str', 'json5-stream'):
        import json5
        # The json5 parse path must not hand the document to the standard json module.
        sys.modules['json'] = None
        if mode == 'json5-bytes':
            value = json5.loads(data)
        elif mode == 'json5-str':
            value = json5.loads(data.decode('utf-8'))
        else:
            value = json5.load(BytesIO(data))
        sys.modules['json'] = json
        report['json5'] = json5.__version__
    else:
        raise SystemExit(f'unknown mode {mode}')
    report['tree'] = tagged(value)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
