"""Print an exact, type-tagged JSON tree for one local file.

Modes: ``pysimdjson-parse`` and ``pysimdjson-load`` call simdjson.Parser().parse(bytes, recursive=True)
and Parser().load(path, recursive=True); stdlib json decoding is disabled while they run.
``stdlib`` is the independent CPython json oracle and must run where pysimdjson is absent.
"""
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


def forbid_stdlib_decoding() -> None:
    # simdjson/__init__.py imports json only for dumps; any decode through it here is a fallback.
    def refuse(*args, **kwargs):
        raise SystemExit('stdlib json decoding was called')
    json.loads = json.load = refuse
    json.decoder.JSONDecoder.decode = json.decoder.JSONDecoder.raw_decode = refuse
    json.decoder.scanstring = json.scanner.make_scanner = refuse


def main() -> None:
    mode, path = sys.argv[1], Path(sys.argv[2])
    data = path.read_bytes()
    report = {'mode': mode}
    if mode == 'stdlib':
        try:
            import simdjson  # noqa: F401
        except ModuleNotFoundError:
            pass
        else:
            raise SystemExit('stdlib oracle must not see pysimdjson')
        pairs_seen = []
        value = json.loads(data, object_pairs_hook=lambda pairs: pairs_seen.append(len(pairs)) or dict(pairs))
        # A shorter dict than its pair list would mean a duplicate key in the control.
        report.update({'python': sys.version.split()[0], 'json_c_scanner': json.scanner.c_make_scanner is not None,
                       'json_c_scanstring': json.decoder.c_scanstring is not None,
                       'object_pairs': sum(pairs_seen)})
    elif mode in ('pysimdjson-parse', 'pysimdjson-load'):
        forbid_stdlib_decoding()
        import csimdjson
        import simdjson
        if simdjson.Parser is not csimdjson.Parser:
            raise SystemExit('simdjson.Parser is not the csimdjson extension type')
        parser = simdjson.Parser()
        value = parser.parse(data, True) if mode == 'pysimdjson-parse' else parser.load(str(path), True)
        report.update({'simdjson': simdjson.VERSION, 'implementation': list(parser.implementation),
                       'compiled_implementations': [name for name, _ in parser.get_implementations(False)],
                       'extension': Path(csimdjson.__file__).name})
    else:
        raise SystemExit(f'unknown mode {mode}')
    report['tree'] = tagged(value)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
