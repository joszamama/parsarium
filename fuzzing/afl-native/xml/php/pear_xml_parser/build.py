"""Build and verify native libxml2 + PHP ext/xml AFL++ feedback for pear/xml_parser (XML_Parser 1.3.8).

Both valid XML controls are checked three ways against the project's expat non-namespace oracle, computed here
independently of PHP and libxml2: the verified coverage image (Xdebug package lines plus LLVM ext/xml and libxml2
lines), and the AFL++-instrumented runtime running the same XML_Parser harness. The AFL++ allowlist limits
instrumentation to libxml2's XML parser sources and ext/xml/xml.c plus ext/xml/compat.c, the same build as the
standard xml_parser_create_ns overlay; the build checks that exactly those objects carry AFL++ edges and that the
ext/xml sources and license files match the manifest hashes.

Each control is probed REPEATS times through three targets: the full harness (JSON output), the fuzz target
(XML_Parser::parse with the summary handler object, no output) and baseline.php, which binds the same handler
object to a bare xml_parser_create()/xml_parse()/xml_parser_free() without any XML_Parser or PEAR code. The gate
requires repeatable maps, a nonzero fuzz-target difference between the controls, and that harness-only and
fuzz-target-only edges are the same for both controls. The receipt records how the package path's differing tuples
relate to the bare baseline's: XML_Parser is interpreted PHP that drives ext/xml, so its input-dependent native
feedback is expected to be ext/xml and libxml2 feedback, not package-owned feedback.
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
    'php-8.5.12/ext/xml/compat.o',
    'php-8.5.12/ext/xml/xml.o',
]
FULL_TARGET = ['/opt/php/bin/php', '/work/harness.php', '/input/case']
PARSE_ONLY_TARGET = ['/opt/php/bin/php', '/work/fuzz-target.php', '/input/case']
BASELINE_TARGET = ['/opt/php/bin/php', '/work/baseline.php', '/input/case']

sys.path.insert(0, str(PROJECT))
sys.dont_write_bytecode = True
from oracle import summarize  # noqa: E402


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
    """Replay one control in the verified coverage image and return its run-control summary."""
    work.mkdir()
    run([*sandbox(case, work, '/input/control'), BASE_IMAGE])
    return json.loads((work / 'summary.json').read_text())


def main() -> None:
    base_receipt = PROJECT / 'verification.json'
    base = json.loads(base_receipt.read_text()) if base_receipt.is_file() else {}
    if not base.get('pass'):
        raise RuntimeError('base PHP project must be verified first')
    controls = {'control': ROOT / MANIFEST['control'],
                'differential': ROOT / MANIFEST['differential_control']}
    digests = {'control': MANIFEST['control_sha256'],
               'differential': MANIFEST['differential_control_sha256']}
    expected = {'control': MANIFEST['expected_output'],
                'differential': MANIFEST['differential_expected_output']}
    for key, path in controls.items():
        if sha256(path.read_bytes()).hexdigest() != digests[key]:
            raise RuntimeError(f'{path} changed')
        if summarize(path.read_bytes()) != expected[key]:
            raise RuntimeError(f'{key}: manifest output differs from the expat oracle')
    base_image_id = run(['docker', 'image', 'inspect', BASE_IMAGE, '--format', '{{.Id}}'])
    if base_image_id != base['image_id']:
        raise RuntimeError('base image differs from the verified project receipt; rerun run_project.py')
    licenses = '\n'.join(f'{digest}  {name}' for name, digest in MANIFEST['license_file_sha256'].items())
    extension_sources = '\n'.join(f'{digest}  {name}' for name, digest in MANIFEST['extension_source_sha256'].items())
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
        if run(['docker', 'run', '--rm', '--entrypoint', 'cat', image, '/work/xml-sources.txt']) != extension_sources:
            raise RuntimeError(f'{image}: ext/xml sources differ from the manifest')
    runtime = run(['docker', 'run', '--rm', '--entrypoint', '/opt/php/bin/php', IMAGE, '-r',
                   'echo PHP_VERSION, " ", LIBXML_DOTTED_VERSION, " ", implode(",", get_loaded_extensions());'])
    php_version, libxml_version, extensions = runtime.split(' ', 2)
    if (php_version, libxml_version) != ('8.5.12', '2.15.4') or 'xml' not in extensions.split(','):
        raise RuntimeError(f'unexpected instrumented runtime: {runtime}')
    instrumented = run(['docker', 'run', '--rm', '--entrypoint', 'cat', IMAGE,
                        '/work/afl-instrumented-objects.txt']).splitlines()
    if instrumented != INSTRUMENTED_OBJECTS:
        raise RuntimeError(f'AFL++ allowlist instrumented other objects: {instrumented}')
    for key, path in controls.items():
        output = json.loads(run([*sandbox(path), '--entrypoint', '/opt/php/bin/php', IMAGE,
                                 '/work/harness.php', '/input/case']))
        bare = json.loads(run([*sandbox(path), '--entrypoint', '/opt/php/bin/php', IMAGE,
                               '/work/baseline.php', '/input/case', '--print']))
        if output != expected[key] or bare != expected[key]:
            raise RuntimeError(f'{key}: instrumented harness or baseline output differs from oracle: {output} {bare}')
    with tempfile.TemporaryDirectory(prefix='parsarium-php-pear-xml-parser-afl-') as temporary:
        work = Path(temporary)
        coverage = {key: base_coverage(path, work / f'base-{key}') for key, path in controls.items()}
        full = {key: stable(path, work, f'full-{key}', FULL_TARGET) for key, path in controls.items()}
        parse = {key: stable(path, work, f'parse-{key}', PARSE_ONLY_TARGET) for key, path in controls.items()}
        bare = {key: stable(path, work, f'bare-{key}', BASELINE_TARGET) for key, path in controls.items()}
    for key in controls:
        if coverage[key]['output'] != expected[key] or not coverage[key]['file_and_stream_api_match']:
            raise RuntimeError(f'{key}: coverage image output differs from oracle')
    if coverage['control']['parser_source_lines_covered'] != base['parser_source_lines_covered']:
        raise RuntimeError('coverage replay differs from the project receipt')
    if len(MAP_SIZES) != 1:
        raise RuntimeError(f'afl-showmap map sizes: {MAP_SIZES}')
    full_edges = {key: edges(value) for key, value in full.items()}
    parse_edges = {key: edges(value) for key, value in parse.items()}
    bare_edges = {key: edges(value) for key, value in bare.items()}
    full_difference = full_edges['control'] ^ full_edges['differential']
    parse_difference = parse_edges['control'] ^ parse_edges['differential']
    bare_difference = bare_edges['control'] ^ bare_edges['differential']
    harness_only = {key: full_edges[key] - parse_edges[key] for key in controls}
    parse_outside_full = {key: parse_edges[key] - full_edges[key] for key in controls}
    package_only = {key: parse_edges[key] - bare_edges[key] for key in controls}
    baseline_only = {key: bare_edges[key] - parse_edges[key] for key in controls}
    if not parse_difference or not bare_difference:
        raise RuntimeError('the two valid controls give the same AFL++ edges')
    for name, extra in (('harness-only', harness_only), ('fuzz-target-only', parse_outside_full)):
        if extra['control'] != extra['differential']:
            raise RuntimeError(f'{name} edges depend on the control')
    # Recorded, not gated: how the package path's input-dependent tuples relate to the bare ext/xml baseline.
    # Edges that only one path reaches include junction edges from the last instrumented block before control
    # returns to interpreted PHP into the next instrumented call, so they can differ per control on either side.
    package_only_varying = package_only['control'] ^ package_only['differential']
    baseline_only_varying = baseline_only['control'] ^ baseline_only['differential']
    lines = lambda key: {field: coverage[key][field] for field in (
        'parser_source_lines_covered', 'format_specific_source_lines_covered', 'support_source_lines_covered',
        'extension_source_lines_covered', 'compat_source_lines_covered',
        'underlying_source_lines_covered', 'underlying_parser_c_lines_covered')}
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'native_libxml2_php_xml_parser_source_edges',
        'feedback_scope': 'libxml2 2.15.4 parser.c (push parser), parserInternals.c and SAX2.c plus PHP 8.5.12 '
                          'ext/xml/xml.c and ext/xml/compat.c (XMLParser API, xml_set_object and handler dispatch, '
                          'expat-compatible SAX callbacks) via AFL++ allowlist; libxml2 tree, XPath and dict code, '
                          'ext/libxml/libxml.c, the Zend engine and the interpreted XML_Parser and PEAR code are '
                          'uninstrumented',
        'fuzz_target': 'projects/xml/php/pear_xml_parser/fuzz-target.php (XML_Parser setInputString and parse with '
                       'the summary handler object, no JSON output)',
        'harness': 'projects/xml/php/pear_xml_parser/harness.php parsarium_parse (XML_Parser setInputString, '
                   'setHandlerObj and parse, then JSON output)',
        'baseline': 'fuzzing/afl-native/xml/php/pear_xml_parser/baseline.php (same handler object bound to a bare '
                    'xml_parser_create/xml_parse, no XML_Parser or PEAR code)',
        'shared_family': 'libxml2 push parser via PHP ext/xml (compat.c), shared with the standard '
                         'xml_parser_create_ns/xml_parse path and the other libxml2 package paths',
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'base_image_id': base_image_id,
        'source_sha256': MANIFEST['source_sha256'],
        'underlying_source_sha256': MANIFEST['underlying_source_sha256'],
        'php_source_sha256': MANIFEST['php_source_sha256'],
        'extension_source_sha256': MANIFEST['extension_source_sha256'],
        'license_file_sha256': MANIFEST['license_file_sha256'],
        'runtime': {'php': php_version, 'libxml2': libxml_version, 'extensions': extensions.split(',')},
        'instrumented_objects': instrumented,
        'control_sha256': MANIFEST['control_sha256'],
        'differential_control_sha256': MANIFEST['differential_control_sha256'],
        'oracle': 'projects/xml/php/pear_xml_parser/oracle.py (expat without namespace processing)',
        'control_output_matches_oracle': True,
        'differential_output_matches_oracle': True,
        'baseline_output_matches_oracle': True,
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
        'format_dependent_parse_time_tuples': len(full_difference & parse_difference),
        'format_dependent_harness_only_tuples': len(full_difference - parse_difference),
        'harness_only_edges': len(harness_only['control']),
        'harness_only_edges_identical': True,
        'parse_only_edges_outside_full_harness': len(parse_outside_full['control']),
        'parse_only_edges_outside_full_harness_identical': True,
        'baseline_control_edges': len(bare['control']),
        'baseline_differential_edges': len(bare['differential']),
        'baseline_tuple_difference': len(bare_difference),
        'differing_tuples_equal_bare_baseline': parse_difference == bare_difference,
        'differing_tuples_subset_of_bare_baseline': parse_difference <= bare_difference,
        'differing_tuples_shared_with_baseline': len(parse_difference & bare_difference),
        'differing_tuples_package_path_only': len(parse_difference - bare_difference),
        'differing_tuples_baseline_only': len(bare_difference - parse_difference),
        'package_path_only_edges': {key: len(value) for key, value in package_only.items()},
        'package_path_only_edges_varying_between_controls': len(package_only_varying),
        'baseline_only_edges': {key: len(value) for key, value in baseline_only.items()},
        'baseline_only_edges_varying_between_controls': len(baseline_only_varying),
        'overlay_file_sha256': {
            name: sha256((OVERLAY / name).read_bytes()).hexdigest()
            for name in ('Dockerfile', 'baseline.php', 'build.py')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {len(parse["control"])}/{len(parse["differential"])} fuzz-target tuples, '
          f'{len(parse_difference)} differ ({len(parse_difference & bare_difference)} shared with the bare '
          f'xml_parse baseline, which differs in {len(bare_difference)}); {REPEATS} identical repeats per control')


if __name__ == '__main__':
    main()
