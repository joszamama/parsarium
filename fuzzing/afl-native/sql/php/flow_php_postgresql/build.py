"""Build and verify native libpg_query + pg_query extension AFL++ feedback for flow-php/postgresql's sql_parse().

Both valid SQL controls are checked three ways against the hand-written summaries in controls/sql/expected.json:
the coverage base image (Xdebug package lines plus LLVM ext/pg_query.c and libpg_query lines), and the
AFL++-instrumented runtime running the full harness and the parse-only fuzz target (sql_parse: the extension's
pg_query_parse_protobuf() and the google/protobuf decode into the package AST classes). The AFL++ allowlist limits
instrumentation to ext/pg_query.c and libpg_query's src_backend_parser_gram.c, src_backend_parser_scan.c and
src_backend_parser_parser.c; PHP is compiled with afl-clang-fast under an allowlist that matches no PHP source. The
build checks that exactly those four objects carry AFL++ edges, that the extension sources and licenses match the
manifest hashes, and that the reflected pg_query_parse_protobuf and sql_parse signatures are the documented ones.
Each control is probed REPEATS times through both targets; the gate requires repeatable maps that differ between
the controls and full harness maps equal to the fuzz-target maps (the Traverser summary walk is interpreted PHP and
runs no instrumented code). The script writes the overlay receipt; scripts/verify_sql_feedback.py then writes
differential.json, including the package PHP lines that /work/afl_trace records.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[5]
OVERLAY = Path(__file__).resolve().parent
RELATIVE = OVERLAY.relative_to(ROOT / 'fuzzing/afl-native')
PROJECT = ROOT / 'projects' / RELATIVE
MANIFEST = json.loads((PROJECT / 'manifest.json').read_text())
IMAGE = f'parsarium-afl/{RELATIVE.parts[0]}-php-{RELATIVE.parts[2]}:local'
BASE_IMAGE = f'parsarium/{RELATIVE.parts[0]}-php-{RELATIVE.parts[2]}:local'
REPEATS = 3
MAP_SIZES: set[str] = set()
INSTRUMENTED_OBJECTS = [
    'libpg_query-18.0.0/src/postgres/src_backend_parser_gram.o',
    'libpg_query-18.0.0/src/postgres/src_backend_parser_parser.o',
    'libpg_query-18.0.0/src/postgres/src_backend_parser_scan.o',
    'pg-query-ext-0.48.0/ext/.libs/pg_query.o',
]
FULL_TARGET = ['/opt/php/bin/php', '/work/harness.php', '/input/case']
PARSE_ONLY_TARGET = ['/work/fuzz-target.php', '/input/case']
API_SIGNATURE = ('pg_query pg_query_parse_protobuf(string $sql): string; '
                 'Flow\\PostgreSql\\DSL\\sql_parse(string $sql): Flow\\PostgreSql\\ParsedQuery')


def run(command: list[str], with_log: bool = False) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'{command[:5]} failed: {(result.stdout + result.stderr)[-3000:]}')
    return (result.stdout + result.stderr) if with_log else result.stdout.strip()


def sandbox(case: Path, work: Path | None = None, mount: str = '/input/case') -> list[str]:
    command = ['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
               '--network', 'none', '--read-only', '--cap-drop', 'ALL',
               '--security-opt', 'no-new-privileges',
               '--user', f'{os.getuid()}:{os.getgid()}',
               '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
               '-v', f'{case}:{mount}:ro']
    return command + (['-v', f'{work}:/coverage'] if work else [])


def showmap(case: Path, work: Path, name: str, target: list[str]) -> frozenset:
    log = run([*sandbox(case, work), '-e', 'AFL_MAP_SIZE=65536', '--entrypoint', 'afl-showmap', IMAGE,
               '-m', 'none', '-t', '30000', '-o', f'/coverage/{name}.map', '--', *target], with_log=True)
    MAP_SIZES.update(re.findall(r'map size (\d+)', log))
    return frozenset(set((work / f'{name}.map').read_text().splitlines()) - {''})


def edges(tuples: frozenset) -> set[str]:
    return {item.split(':', 1)[0] for item in tuples}


def stable(case: Path, work: Path, name: str, target: list[str]) -> frozenset:
    maps = [showmap(case, work, f'{name}{index}', target) for index in range(REPEATS)]
    if len(set(maps)) != 1:
        raise RuntimeError(f'{name}: repeated AFL++ maps differ')
    return maps[0]


def base_coverage(case: Path, work: Path) -> dict:
    """Replay one control in the LLVM-coverage base image and return its run-control summary."""
    work.mkdir()
    os.chmod(work, 0o777)
    run([*sandbox(case, work, '/input/control'), BASE_IMAGE])
    return json.loads((work / 'summary.json').read_text())


def main() -> None:
    base_receipt = PROJECT / 'verification.json'
    if not base_receipt.is_file() or not json.loads(base_receipt.read_text()).get('pass'):
        raise RuntimeError('base flow-php/postgresql project must be verified first')
    base = json.loads(base_receipt.read_text())
    oracle = json.loads((ROOT / 'controls/sql/expected.json').read_text())['controls']
    controls = {'control': ROOT / MANIFEST['control'],
                'differential': ROOT / MANIFEST['differential_control']}
    digests = {'control': MANIFEST['control_sha256'],
               'differential': MANIFEST['differential_control_sha256']}
    expected = {'control': MANIFEST['expected_output'],
                'differential': MANIFEST['differential_expected_output']}
    for key, path in controls.items():
        if sha256(path.read_bytes()).hexdigest() != digests[key]:
            raise RuntimeError(f'{path} changed')
        if oracle[path.name] != expected[key]:
            raise RuntimeError(f'{key}: manifest summary differs from the SQL oracle')
    licenses = '\n'.join(f'{digest}  {name}' for name, digest in MANIFEST['license_file_sha256'].items())
    extension_sources = '\n'.join(f'{digest}  {name}'
                                  for name, digest in MANIFEST['extension_source_sha256'].items())
    base_image_id = run(['docker', 'image', 'inspect', BASE_IMAGE, '--format', '{{.Id}}'])
    if base_image_id != base['image_id']:
        raise RuntimeError('base image differs from the verified project receipt; rerun run_project.py')
    run(['docker', 'build', '--quiet', '--platform', MANIFEST['platform'],
         '-f', str(OVERLAY / 'Dockerfile'), '-t', IMAGE, str(ROOT)])
    image_id = run(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}'])
    version = run(['docker', 'run', '--rm', '--entrypoint', 'dpkg-query', IMAGE,
                   '-W', '-f=${Version}', 'afl++'])
    if version != MANIFEST['fuzz_engine_release']:
        raise RuntimeError(f'AFL++ version mismatch: {version}')
    for image in (BASE_IMAGE, IMAGE):
        if run(['docker', 'run', '--rm', '--entrypoint', 'cat', image, '/work/licenses.txt']) != licenses:
            raise RuntimeError(f'{image}: license files differ from the manifest')
        if run(['docker', 'run', '--rm', '--entrypoint', 'cat', image,
                '/work/pg-query-ext-sources.txt']) != extension_sources:
            raise RuntimeError(f'{image}: pg-query-ext sources differ from the manifest')
    runtime = run(['docker', 'run', '--rm', '--entrypoint', '/opt/php/bin/php', IMAGE, '-r',
                   'echo PHP_VERSION, " ", phpversion("pg_query"), " ", implode(",", get_loaded_extensions());'])
    php_version, extension_version, extensions = runtime.split(' ', 2)
    if (php_version, extension_version) != ('8.5.12', '0.48.0') or 'pg_query' not in extensions.split(','):
        raise RuntimeError(f'unexpected instrumented runtime: {runtime}')
    info = run(['docker', 'run', '--rm', '--entrypoint', '/opt/php/bin/php', IMAGE, '--ri', 'pg_query'])
    if not re.search(r'libpg_query version => 18\.0\.0$', info, re.M):
        raise RuntimeError(f'unexpected libpg_query version: {info}')
    signature = run(['docker', 'run', '--rm', '--entrypoint', '/opt/php/bin/php', IMAGE, '-r',
                     'require "/work/vendor/autoload.php"; $out = []; '
                     'foreach (["pg_query_parse_protobuf", "Flow\\\\PostgreSql\\\\DSL\\\\sql_parse"] as $name) { '
                     '$f = new ReflectionFunction($name); '
                     '$out[] = ($f->getExtensionName() ? $f->getExtensionName() . " " : "") . $f->getName() . "(" . '
                     'implode(",", array_map(fn ($p) => ltrim($p->getType() . " $" . $p->getName()), '
                     '$f->getParameters())) . "): " . $f->getReturnType(); } echo implode("; ", $out);'])
    if signature != API_SIGNATURE:
        raise RuntimeError(f'unexpected API signatures: {signature}')
    instrumented = run(['docker', 'run', '--rm', '--entrypoint', 'cat', IMAGE,
                        '/work/afl-instrumented-objects.txt']).splitlines()
    if instrumented != INSTRUMENTED_OBJECTS:
        raise RuntimeError(f'AFL++ allowlist instrumented other objects: {instrumented}')
    for key, path in controls.items():
        output = json.loads(run([*sandbox(path), '--entrypoint', '/opt/php/bin/php', IMAGE,
                                 '/work/harness.php', '/input/case']))
        if output != expected[key]:
            raise RuntimeError(f'{key}: instrumented harness output differs from oracle: {output}')
    with tempfile.TemporaryDirectory(prefix='parsarium-flow-postgresql-afl-') as temporary:
        work = Path(temporary)
        os.chmod(work, 0o777)
        coverage = {key: base_coverage(path, work / f'base-{key}') for key, path in controls.items()}
        full = {key: stable(path, work, f'full-{key}', FULL_TARGET) for key, path in controls.items()}
        parse = {key: stable(path, work, f'parse-{key}', PARSE_ONLY_TARGET) for key, path in controls.items()}
    for key in controls:
        if coverage[key]['output'] != expected[key]:
            raise RuntimeError(f'{key}: LLVM-coverage base output differs from oracle')
    for field in ('parser_source_lines_covered', 'underlying_source_lines_covered'):
        if coverage['control'][field] != base[field]:
            raise RuntimeError(f'base coverage replay differs from the project receipt: {field}')
    if MAP_SIZES != {'65536'}:
        raise RuntimeError(f'afl-showmap map sizes: {MAP_SIZES}')
    full_edges = {key: edges(value) for key, value in full.items()}
    parse_edges = {key: edges(value) for key, value in parse.items()}
    parse_difference = parse_edges['control'] ^ parse_edges['differential']
    full_difference = full_edges['control'] ^ full_edges['differential']
    if not parse_difference:
        raise RuntimeError('fuzz-target feedback does not differ between the controls')
    if full != parse:
        raise RuntimeError('full harness maps differ from the parse-only fuzz-target maps')
    lines = lambda key: {field: coverage[key][field] for field in (
        'parser_source_lines_covered', 'format_specific_source_lines_covered',
        'support_source_lines_covered', 'extension_source_lines_covered',
        'underlying_source_lines_covered', 'underlying_libpg_query_lines_covered',
        'underlying_gram_c_lines_covered')}
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'native_libpg_query_php_pg_query_parser_source_edges',
        'feedback_scope': 'pg-query-ext 0.48.0 ext/pg_query.c (pg_query_parse_protobuf) plus libpg_query 18.0.0 '
                          'src_backend_parser_gram.c, src_backend_parser_scan.c and src_backend_parser_parser.c '
                          'via AFL++ allowlist while flow-php/postgresql decodes the protobuf tree in PHP; the '
                          'protobuf output functions, the rest of libpg_query, the PHP runtime and the interpreted '
                          'package and google/protobuf code are uninstrumented (package lines: /work/afl_trace)',
        'fuzz_target': 'projects/sql/php/flow_php_postgresql/fuzz-target.php (sql_parse only: native parse and '
                       'protobuf decode into the package AST classes, no Traverser summary)',
        'harness': 'projects/sql/php/flow_php_postgresql/harness.php (sql_parse, then the package Traverser with '
                   'the summary NodeVisitor)',
        'extension_source_sha256': MANIFEST['extension_source_sha256'],
        'api_signature': signature,
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'base_image_id': base_image_id,
        'source_sha256': MANIFEST['source_sha256'],
        'underlying_source_sha256': MANIFEST['underlying_source_sha256'],
        'php_source_sha256': MANIFEST['php_source_sha256'],
        'license_file_sha256': MANIFEST['license_file_sha256'],
        'runtime': {'php': php_version, 'pg_query_ext': extension_version, 'libpg_query': '18.0.0',
                    'flow_php_postgresql': '0.48.0', 'google_protobuf': 'v5.36.2'},
        'package_license_file_sha256': MANIFEST['package_license_file_sha256'],
        'instrumented_objects': instrumented,
        'control_sha256': MANIFEST['control_sha256'],
        'differential_control_sha256': MANIFEST['differential_control_sha256'],
        'oracle': 'controls/sql/expected.json hand-written summaries (cross-checked with SQLite by '
                  'controls/sql/check_controls.py)',
        'control_output_matches_oracle': True,
        'differential_output_matches_oracle': True,
        'base_coverage_lines': {'control': lines('control'), 'differential': lines('differential')},
        'control_package_lines_by_file': coverage['control']['package_lines_by_file'],
        'differential_package_lines_by_file': coverage['differential']['package_lines_by_file'],
        'image_id': image_id, 'platform': MANIFEST['platform'],
        'afl_package': version,
        # Pinned: AFL_MAP_SIZE=65536 is passed to afl-showmap and its log reports that size for every run.
        'afl_map_size': 65536,
        'repeats_per_control': REPEATS,
        'all_repeats_identical': True,
        'feedback_edges': len(parse['control']),
        'differential_feedback_edges': len(parse['differential']),
        'stable_shared_edges': len(parse_edges['control'] & parse_edges['differential']),
        'stable_control_only_edges': len(parse_edges['control'] - parse_edges['differential']),
        'stable_differential_only_edges': len(parse_edges['differential'] - parse_edges['control']),
        'afl_tuple_difference': len(parse_difference),
        'full_harness_control_edges': len(full['control']),
        'full_harness_differential_edges': len(full['differential']),
        'full_harness_tuple_difference': len(full_difference),
        'full_harness_maps_equal_fuzz_target': True,
        'overlay_file_sha256': {
            name: sha256((OVERLAY / name).read_bytes()).hexdigest()
            for name in ('Dockerfile', 'build.py', 'afl_trace', 'afl_trace.php')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {len(parse["control"])}/{len(parse["differential"])} fuzz-target tuples, '
          f'{len(parse_difference)} differ; full harness maps equal; {REPEATS} identical repeats per control')


if __name__ == '__main__':
    main()
