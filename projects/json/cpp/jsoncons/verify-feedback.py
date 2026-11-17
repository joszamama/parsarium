"""Audit native jsoncons parser coverage and AFL++ feedback on two valid controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[4]
PROJECT = Path(__file__).resolve().parent
OVERLAY = ROOT / 'fuzzing/afl-native/json/cpp/jsoncons'
MANIFEST = json.loads((PROJECT / 'manifest.json').read_text())
BASE = json.loads((PROJECT / 'verification.json').read_text())
AFL = json.loads((OVERLAY / 'verification.json').read_text())


def run(command):
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-3000:])
    return result.stdout


def lines(path):
    coverage = json.loads(path.read_text())
    return {f'{f["filename"]}:{segment[0]}'
            for f in coverage['data'][0]['files']
            if f['filename'].endswith('/source/include/jsoncons/json_parser.hpp')
            for segment in f['segments'] if segment[2] and segment[3] > 0}


def typed_tree(text):
    def canon(value):
        if isinstance(value, tuple):
            if value[0] == 'object':
                return ('object', tuple(sorted((key, canon(child)) for key, child in value[1])))
            return value
        if isinstance(value, list): return ('array', tuple(canon(child) for child in value))
        if value is None: return ('null',)
        if isinstance(value, bool): return ('boolean', value)
        return ('string', value)
    parsed = json.loads(text,
                        object_pairs_hook=lambda pairs: ('object', tuple(pairs)),
                        parse_int=lambda raw: ('integer', int(raw)),
                        parse_float=lambda raw: ('float', float(raw)))
    return canon(parsed)


def main():
    if AFL['base_project_receipt_sha256'] != sha256((PROJECT / 'verification.json').read_bytes()).hexdigest():
        raise RuntimeError('AFL++ overlay refers to a different project receipt')
    controls = [(MANIFEST['control'], MANIFEST['control_sha256'], MANIFEST['expected_output']),
                (MANIFEST['differential_control'], MANIFEST['differential_control_sha256'],
                 MANIFEST['differential_expected_output'])]
    results = []
    outputs = []
    with tempfile.TemporaryDirectory(prefix='parsarium-jsoncons-') as tmp:
        output = Path(tmp)
        for index, (name, expected_hash, expected_output) in enumerate(controls):
            case = ROOT / name
            if sha256(case.read_bytes()).hexdigest() != expected_hash:
                raise RuntimeError(f'control changed: {name}')
            attempts = []
            for repeat in range(3):
                key = f'{index}-{repeat}'
                sandbox = ['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                           '--network', 'none', '--read-only', '--cap-drop', 'ALL',
                           '--security-opt', 'no-new-privileges',
                           '--user', f'{os.getuid()}:{os.getgid()}',
                           '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
                           '-v', f'{case}:/input/case:ro', '-v', f'{output}:/coverage']
                observed_text = run([*sandbox, '--entrypoint', '/work/replay',
                                     BASE['image_id'], '/input/case'])
                observed = json.loads(observed_text)
                if (observed != expected_output or
                        typed_tree(observed_text) != typed_tree(case.read_text())):
                    raise RuntimeError(f'exact typed JSON tree mismatch: {name}: {observed}')
                if repeat == 0:
                    outputs.append(observed)
                script = ('set -eu; LLVM_PROFILE_FILE=/tmp/case.profraw '
                          '/work/parser-probe /input/case; '
                          'llvm-profdata merge -sparse /tmp/case.profraw -o /tmp/case.profdata; '
                          f'llvm-cov export /work/parser-probe -instr-profile=/tmp/case.profdata > /coverage/{key}.json')
                run([*sandbox, '--entrypoint', '/bin/sh', BASE['image_id'], '-c', script])
                source_lines = lines(output / f'{key}.json')
                if not source_lines:
                    raise RuntimeError('no jsoncons parser source lines covered')
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
        'project': 'json/cpp/jsoncons', 'pass': True,
        'feedback_kind': 'afl_clang_fast_jsoncons_parser_header_only_edges_and_source_lines',
        'probe': 'projects/json/cpp/jsoncons/parser-probe.cpp',
        'probe_scope': 'json::parse(const char*, size_t) only; no tree traversal, serialization, or result formatting',
        'base_project_receipt_sha256': sha256((PROJECT / 'verification.json').read_bytes()).hexdigest(),
        'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
        'base_image_id': BASE['image_id'], 'overlay_image_id': AFL['image_id'],
        'afl_package': AFL['afl_package'], 'afl_map_size': AFL['afl_map_size'],
        'allowlist': 'projects/json/cpp/jsoncons/afl-allowlist.txt',
        'repeats_per_control': 3,
        'first_control': controls[0][0], 'second_control': controls[1][0],
        'first_observed_output': outputs[0], 'second_observed_output': outputs[1],
        'first_parser_lines': len(results[0][0]), 'second_parser_lines': len(results[1][0]),
        'parser_line_difference': line_diff,
        'first_afl_tuples': len(results[0][1]), 'second_afl_tuples': len(results[1][1]),
        'afl_tuple_difference': tuple_diff, 'repeated_feedback_identical': True,
        'second_case_kind': 'valid_control',
    }
    (OVERLAY / 'differential.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record))


if __name__ == '__main__':
    main()
