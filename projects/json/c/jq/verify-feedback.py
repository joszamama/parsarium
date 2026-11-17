"""Audit parser-scoped coverage and AFL++ feedback for this C JSON path on two valid controls.

The replay prints the parsed tree, which must equal Python json.loads of each control with
key order and integer/float kinds. The parser-only probe (parse and free, no printing) gives
own-library source lines under LLVM coverage and AFL++ tuples under a parser-scoped allowlist.
Each control is probed three times; repeats must be identical and the controls must differ.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[4]
PROJECT = Path(__file__).resolve().parent
SLUG = PROJECT.name
OVERLAY = ROOT / 'fuzzing/afl-native/json/c' / SLUG
MANIFEST = json.loads((PROJECT / 'manifest.json').read_text())
BASE = json.loads((PROJECT / 'verification.json').read_text())
AFL = json.loads((OVERLAY / 'verification.json').read_text())
PREFIX = MANIFEST['coverage_subject_prefix']
REPEATS = 3


def run(command):
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-3000:])
    return result.stdout


def lines(path):
    coverage = json.loads(path.read_text())
    return {f'{f["filename"].removeprefix(PREFIX)}:{segment[0]}'
            for f in coverage['data'][0]['files'] if f['filename'].startswith(PREFIX)
            for segment in f['segments'] if segment[2] and segment[3] > 0}


def typed_tree(text):
    # Order-preserving, kind-aware view: 1 and 1.0 or reordered keys do not match.
    def canon(value):
        if isinstance(value, tuple): return ('object', [(key, canon(child)) for key, child in value[1]])
        if isinstance(value, list): return ('array', [canon(child) for child in value])
        return (type(value).__name__, value)
    return canon(json.loads(text, object_pairs_hook=lambda pairs: ('object', pairs)))


def summarize_tree(value):
    result = {'arrays': 0, 'booleans': 0, 'max_depth': 0,
              'nulls': 0, 'numbers': [], 'objects': 0, 'strings': []}
    def walk(node, depth):
        if isinstance(node, dict):
            result['objects'] += 1
            result['max_depth'] = max(result['max_depth'], depth)
            for child in node.values(): walk(child, depth + 1)
        elif isinstance(node, list):
            result['arrays'] += 1
            result['max_depth'] = max(result['max_depth'], depth)
            for child in node: walk(child, depth + 1)
        elif node is None: result['nulls'] += 1
        elif isinstance(node, bool): result['booleans'] += 1
        elif isinstance(node, (int, float)): result['numbers'].append(node)
        elif isinstance(node, str): result['strings'].append(node)
    walk(value, 1)
    result['numbers'].sort(); result['strings'].sort()
    result['root'] = 'object' if isinstance(value, dict) else 'array'
    if isinstance(value, dict): result['top_level_keys'] = sorted(value)
    else: result['top_level_items'] = len(value)
    return result


def by_file(items):
    counts = {}
    for item in items:
        name = item.rsplit(':', 1)[0]
        counts[name] = counts.get(name, 0) + 1
    return dict(sorted(counts.items()))


def main():
    if AFL['base_project_receipt_sha256'] != sha256((PROJECT / 'verification.json').read_bytes()).hexdigest():
        raise RuntimeError('AFL++ overlay refers to a different project receipt')
    instrumented = run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                        '--entrypoint', 'cat', AFL['image_id'],
                        '/work/afl-instrumented-objects.txt']).split()
    controls = [(MANIFEST['control'], MANIFEST['control_sha256'], MANIFEST['expected_output']),
                (MANIFEST['differential_control'], MANIFEST['differential_control_sha256'],
                 MANIFEST['differential_expected_output'])]
    results, outputs = [], []
    with tempfile.TemporaryDirectory(prefix=f'parsarium-{SLUG}-') as tmp:
        output = Path(tmp)
        for index, (name, expected_hash, expected_output) in enumerate(controls):
            case = ROOT / name
            if sha256(case.read_bytes()).hexdigest() != expected_hash:
                raise RuntimeError(f'control changed: {name}')
            attempts = []
            for repeat in range(REPEATS):
                key = f'{index}-{repeat}'
                sandbox = ['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                           '--network', 'none', '--read-only', '--cap-drop', 'ALL',
                           '--security-opt', 'no-new-privileges',
                           '--user', f'{os.getuid()}:{os.getgid()}',
                           '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
                           '-v', f'{case}:/input/case:ro', '-v', f'{output}:/coverage']
                observed_text = run([*sandbox, '-e', 'LLVM_PROFILE_FILE=/tmp/replay.profraw',
                                     '--entrypoint', '/work/replay', BASE['image_id'], '/input/case'])
                if typed_tree(observed_text) != typed_tree(case.read_text()):
                    raise RuntimeError(f'exact ordered typed JSON tree mismatch: {name}')
                observed = summarize_tree(json.loads(observed_text))
                if observed != expected_output:
                    raise RuntimeError(f'format-aware summary differs from manifest: {name}: {observed}')
                if repeat == 0:
                    outputs.append(observed)
                script = ('set -eu; LLVM_PROFILE_FILE=/tmp/case.profraw '
                          '/work/parser-probe /input/case; '
                          'llvm-profdata merge -sparse /tmp/case.profraw -o /tmp/case.profdata; '
                          f'llvm-cov export /work/parser-probe -instr-profile=/tmp/case.profdata > /coverage/{key}.json')
                run([*sandbox, '--entrypoint', '/bin/sh', BASE['image_id'], '-c', script])
                source_lines = lines(output / f'{key}.json')
                if not source_lines:
                    raise RuntimeError(f'no {SLUG} parser source lines covered')
                run([*sandbox, '-e', f'AFL_MAP_SIZE={AFL["afl_map_size"]}',
                     '--workdir', '/tmp', '--entrypoint', 'afl-showmap', AFL['image_id'],
                     '-m', 'none', '-t', '10000', '-o', f'/coverage/{key}.map',
                     '--', '/work/parser-probe', '/input/case'])
                tuples = {line.split(':', 1)[0] for line in
                          (output / f'{key}.map').read_text().splitlines() if line}
                if not tuples:
                    raise RuntimeError('no parser-only AFL++ tuples')
                attempts.append((source_lines, tuples))
            if any(attempts[0] != attempt for attempt in attempts[1:]):
                raise RuntimeError(f'feedback varied on repeated {name}')
            results.append(attempts[0])
    line_diff = len(results[0][0] ^ results[1][0])
    tuple_diff = len(results[0][1] ^ results[1][1])
    if not line_diff or not tuple_diff:
        raise RuntimeError('valid controls did not differ in parser source and AFL++ feedback')
    record = {
        'schema_version': 1, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'project': f'json/c/{SLUG}', 'pass': True,
        'feedback_kind': 'afl_clang_fast_parser_scoped_edges_and_source_lines',
        'probe': f'projects/json/c/{SLUG}/parser-probe.c',
        'probe_scope': 'parse the local bytes and free the result; no tree traversal, printing, or result formatting',
        'dom_oracle': 'python_json_loads_order_and_number_kind_preserving',
        'exact_tree_outputs_verified': True,
        'base_project_receipt_sha256': sha256((PROJECT / 'verification.json').read_bytes()).hexdigest(),
        'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
        'base_image_id': BASE['image_id'], 'overlay_image_id': AFL['image_id'],
        'afl_package': AFL['afl_package'], 'afl_map_size': AFL['afl_map_size'],
        'allowlist': f'projects/json/c/{SLUG}/afl-allowlist.txt',
        'allowlist_entries': [line for line in (PROJECT / 'afl-allowlist.txt').read_text().splitlines() if line],
        'afl_instrumented_objects': instrumented,
        'source_line_scope': f'covered lines under {PREFIX} in the parser-only probe',
        'repeats_per_control': REPEATS,
        'first_control': controls[0][0], 'second_control': controls[1][0],
        'first_tree_output': outputs[0], 'second_tree_output': outputs[1],
        'first_parser_lines': len(results[0][0]), 'second_parser_lines': len(results[1][0]),
        'parser_line_difference': line_diff,
        'first_only_lines_by_file': by_file(results[0][0] - results[1][0]),
        'second_only_lines_by_file': by_file(results[1][0] - results[0][0]),
        'first_afl_tuples': len(results[0][1]), 'second_afl_tuples': len(results[1][1]),
        'afl_tuple_difference': tuple_diff, 'repeated_feedback_identical': True,
        'second_case_kind': 'valid_control',
    }
    (OVERLAY / 'differential.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record))


if __name__ == '__main__':
    main()
