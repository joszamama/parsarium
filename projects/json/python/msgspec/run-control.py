"""Replay controls/json/nested-object.json through msgspec.json.decode(bytes)."""
import json
from pathlib import Path
from harness import parse_json

observed = parse_json(Path('/input/control').read_bytes())
# Written by hand from the control text; -0.25e1 is the float -2.5 and é is é.
expected = {'value': ['object', [
    ['name', ['string', 'parsarium']],
    ['version', ['int', 1]],
    ['ratio', ['float', '-2.5']],
    ['enabled', ['bool', True]],
    ['missing', ['null']],
    ['tags', ['array', [['string', 'json'], ['string', 'go'], ['string', 'rfc8259']]]],
    ['nested', ['object', [
        ['level', ['int', 2]],
        ['items', ['array', [
            ['object', [['id', ['int', 1]], ['ok', ['bool', False]]]],
            ['object', [['id', ['int', 2]], ['text', ['string', 'café "quoted"']]]]]]],
        ['empty', ['object', []]],
        ['list', ['array', []]]]]]]]}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2, ensure_ascii=False) + '\n')
