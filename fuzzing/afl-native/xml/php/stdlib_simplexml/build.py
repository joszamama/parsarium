"""Build and verify native libxml2 + PHP ext/simplexml AFL++ feedback for simplexml_load_string.

Both valid XML controls are checked three ways against an expat oracle computed here, independently of PHP
and libxml2: the LLVM-coverage base image (which also records ext/simplexml simplexml.c and libxml2 parser.c
lines for the second control), and the AFL++-instrumented runtime running the same SimpleXML harness. The
AFL++ allowlist limits instrumentation to libxml2's XML parser sources and ext/simplexml/simplexml.c; the
build checks that exactly those objects carry AFL++ edges and that the SimpleXML sources match the manifest
hashes. Each control is probed REPEATS times through the parse-only fuzz target (simplexml_load_string only),
which is what AFL++ runs, and through the full harness (load plus SimpleXML traversal). simplexml.c also holds
the traversal methods, so the full harness adds tuples the fuzz target never reaches; they are counted in the
receipt. The gate requires the parse-only maps to be repeatable and to differ between the controls, and any
parse-only edge the full harness does not reach (the fuzz target discards its SimpleXMLElement at once rather
than at shutdown) to be the same for both controls, so it cannot carry input-dependent feedback.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[5]
OVERLAY = Path(__file__).resolve().parent
RELATIVE = OVERLAY.relative_to(ROOT / 'fuzzing/afl-native')
PROJECT = ROOT / 'projects' / RELATIVE
MANIFEST = json.loads((PROJECT / 'manifest.json').read_text())
IMAGE = f'parsarium-afl/{RELATIVE.parts[0]}-php-{RELATIVE.parts[2]}:local'
BASE_IMAGE = f'parsarium/{RELATIVE.parts[0]}-php-{RELATIVE.parts[2]}:local'
REPEATS = 5
MAP_SIZES: set[str] = set()
INSTRUMENTED_OBJECTS = [
    'libxml2-2.15.4/build/.libs/libxml2_la-SAX2.o',
    'libxml2-2.15.4/build/.libs/libxml2_la-parser.o',
    'libxml2-2.15.4/build/.libs/libxml2_la-parserInternals.o',
    'php-8.5.12/ext/simplexml/simplexml.o',
]
FULL_TARGET = ['/opt/php/bin/php', '/work/harness.php', '/input/case']
PARSE_ONLY_TARGET = ['/opt/php/bin/php', '/work/fuzz-target.php', '/input/case']
API_SIGNATURE = ('SimpleXML string $data,?string $class_name,int $options,string $namespace_or_prefix,'
                 'bool $is_prefix SimpleXMLElement|false')

sys.path.insert(0, str(ROOT / 'controls/xml'))
from check_controls import summarize  # noqa: E402


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
    run([*sandbox(case, work, '/input/control'), BASE_IMAGE])
    return json.loads((work / 'summary.json').read_text())


def main() -> None:
    base_receipt = PROJECT / 'verification.json'
    if not base_receipt.is_file() or not json.loads(base_receipt.read_text()).get('pass'):
        raise RuntimeError('base PHP runtime project must be verified first')
    base = json.loads(base_receipt.read_text())
    controls = {'control': ROOT / MANIFEST['control'],
                'differential': ROOT / MANIFEST['differential_control']}
    digests = {'control': MANIFEST['control_sha256'],
               'differential': MANIFEST['differential_control_sha256']}
    for key, path in controls.items():
        if sha256(path.read_bytes()).hexdigest() != digests[key]:
            raise RuntimeError(f'{path} changed')
    expected = {'control': MANIFEST['expected_output'],
                'differential': MANIFEST['differential_expected_output']}
    for key, path in controls.items():
        if summarize(path.read_bytes()) != expected[key]:
            raise RuntimeError(f'{key}: manifest output differs from the expat oracle')
    licenses = '\n'.join(f'{digest}  {name}' for name, digest in MANIFEST['license_file_sha256'].items())
    base_image_id = run(['docker', 'image', 'inspect', BASE_IMAGE, '--format', '{{.Id}}'])
    if base_image_id != base['image_id']:
        raise RuntimeError('base image differs from the verified project receipt; rerun run_project.py')
    if run(['docker', 'run', '--rm', '--entrypoint', 'cat', BASE_IMAGE, '/work/licenses.txt']) != licenses:
        raise RuntimeError('base image license files differ from the manifest')
    run(['docker', 'build', '--quiet', '--platform', MANIFEST['platform'],
         '-f', str(OVERLAY / 'Dockerfile'), '-t', IMAGE, str(ROOT)])
    image_id = run(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}'])
    version = run(['docker', 'run', '--rm', '--entrypoint', 'dpkg-query', IMAGE,
                   '-W', '-f=${Version}', 'afl++'])
    if version != MANIFEST['fuzz_engine_release']:
        raise RuntimeError(f'AFL++ version mismatch: {version}')
    if run(['docker', 'run', '--rm', '--entrypoint', 'cat', IMAGE, '/work/licenses.txt']) != licenses:
        raise RuntimeError('overlay license files differ from the manifest')
    runtime = run(['docker', 'run', '--rm', '--entrypoint', '/opt/php/bin/php', IMAGE, '-r',
                   'echo PHP_VERSION, " ", LIBXML_DOTTED_VERSION, " ", implode(",", get_loaded_extensions());'])
    php_version, libxml_version, extensions = runtime.split(' ', 2)
    if (php_version, libxml_version) != ('8.5.12', '2.15.4') or 'SimpleXML' not in extensions.split(','):
        raise RuntimeError(f'unexpected instrumented runtime: {runtime}')
    extension_sources = '\n'.join(f'{digest}  {name}' for name, digest in MANIFEST['extension_source_sha256'].items())
    for image in (BASE_IMAGE, IMAGE):
        if run(['docker', 'run', '--rm', '--entrypoint', 'cat', image, '/work/simplexml-sources.txt']) != extension_sources:
            raise RuntimeError(f'{image}: ext/simplexml sources differ from the manifest')
    signature = run(['docker', 'run', '--rm', '--entrypoint', '/opt/php/bin/php', IMAGE, '-r',
                     '$f = new ReflectionFunction("simplexml_load_string"); echo $f->getExtensionName(), " ", '
                     'implode(",", array_map(fn ($p) => $p->getType() . " $" . $p->getName(), $f->getParameters())), '
                     '" ", $f->getReturnType();'])
    if signature != API_SIGNATURE:
        raise RuntimeError(f'unexpected simplexml_load_string signature: {signature}')
    instrumented = run(['docker', 'run', '--rm', '--entrypoint', 'cat', IMAGE,
                        '/work/afl-instrumented-objects.txt']).splitlines()
    if instrumented != INSTRUMENTED_OBJECTS:
        raise RuntimeError(f'AFL++ allowlist instrumented other objects: {instrumented}')
    outputs = {}
    for key, path in controls.items():
        outputs[key] = json.loads(run([*sandbox(path), '--entrypoint', '/opt/php/bin/php', IMAGE,
                                       '/work/harness.php', '/input/case']))
        if outputs[key] != expected[key]:
            raise RuntimeError(f'{key}: instrumented harness output differs from oracle: {outputs[key]}')
    with tempfile.TemporaryDirectory(prefix='parsarium-php-simplexml-afl-') as temporary:
        work = Path(temporary)
        coverage = {key: base_coverage(path, work / f'base-{key}') for key, path in controls.items()}
        full = {key: stable(path, work, f'full-{key}', FULL_TARGET) for key, path in controls.items()}
        parse = {key: stable(path, work, f'parse-{key}', PARSE_ONLY_TARGET) for key, path in controls.items()}
    for key in controls:
        if coverage[key]['output'] != expected[key]:
            raise RuntimeError(f'{key}: LLVM-coverage base output differs from oracle')
    if coverage['control']['parser_source_lines_covered'] != base['parser_source_lines_covered']:
        raise RuntimeError('base coverage replay differs from the project receipt')
    if len(MAP_SIZES) != 1:
        raise RuntimeError(f'afl-showmap map sizes: {MAP_SIZES}')
    full_edges = {key: edges(value) for key, value in full.items()}
    parse_edges = {key: edges(value) for key, value in parse.items()}
    full_difference = full_edges['control'] ^ full_edges['differential']
    parse_difference = parse_edges['control'] ^ parse_edges['differential']
    post_parse = {key: full_edges[key] - parse_edges[key] for key in controls}
    parse_attributed = full_difference & parse_difference
    traversal_only = full_difference - parse_difference
    parse_only = {key: parse_edges[key] - full_edges[key] for key in controls}
    if not parse_difference or parse_only['control'] != parse_only['differential']:
        raise RuntimeError(f'parse-only feedback is empty or has input-dependent edges outside the full harness: '
                           f'{len(parse_difference)} parse-time tuples differ')
    lines = lambda key: {field: coverage[key][field] for field in (
        'parser_source_lines_covered', 'format_specific_source_lines_covered',
        'underlying_source_lines_covered', 'underlying_parser_c_lines_covered', 'underlying_sax2_c_lines_covered')}
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'native_libxml2_php_simplexml_parser_source_edges',
        'feedback_scope': 'libxml2 2.15.4 parser.c, parserInternals.c and SAX2.c plus PHP 8.5.12 '
                          'ext/simplexml/simplexml.c (simplexml_load_string and SimpleXMLElement) via AFL++ '
                          'allowlist; libxml2 tree, XPath and dict code, ext/libxml/libxml.c and the Zend '
                          'engine are uninstrumented',
        'fuzz_target': 'projects/xml/php/stdlib_simplexml/fuzz-target.php (simplexml_load_string only)',
        'harness': 'projects/xml/php/stdlib_simplexml/harness.php (simplexml_load_string, then summary.php '
                   'SimpleXML traversal)',
        'extension_source_sha256': MANIFEST['extension_source_sha256'],
        'api_signature': signature,
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'base_image_id': base_image_id,
        'source_sha256': MANIFEST['source_sha256'],
        'underlying_source_sha256': MANIFEST['underlying_source_sha256'],
        'license_file_sha256': MANIFEST['license_file_sha256'],
        'runtime': {'php': php_version, 'libxml2': libxml_version},
        'instrumented_objects': instrumented,
        'control_sha256': MANIFEST['control_sha256'],
        'differential_control_sha256': MANIFEST['differential_control_sha256'],
        'oracle': 'controls/xml/check_controls.py expat namespace-mode summary',
        'control_output_matches_oracle': True,
        'differential_output_matches_oracle': True,
        'base_coverage_lines': {'control': lines('control'), 'differential': lines('differential')},
        'image_id': image_id, 'platform': MANIFEST['platform'],
        'afl_package': version, 'afl_map_size': int(next(iter(MAP_SIZES))),
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
        'format_dependent_parse_time_tuples': len(parse_attributed),
        'format_dependent_traversal_only_tuples': len(traversal_only),
        'post_parse_control_edges': len(post_parse['control']),
        'post_parse_differential_edges': len(post_parse['differential']),
        'post_parse_edges_identical': post_parse['control'] == post_parse['differential'],
        'parse_only_edges_outside_full_harness': len(parse_only['control']),
        'parse_only_edges_outside_full_harness_identical': True,
        'overlay_file_sha256': {
            name: sha256((OVERLAY / name).read_bytes()).hexdigest()
            for name in ('Dockerfile', 'build.py')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {len(parse["control"])}/{len(parse["differential"])} parse-only tuples, '
          f'{len(parse_difference)} differ; full harness differs in {len(full_difference)} '
          f'({len(traversal_only)} traversal-only); {REPEATS} identical repeats per control')


if __name__ == '__main__':
    main()
