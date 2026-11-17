"""Build and verify native libyaml + pecl/yaml AFL++ feedback for yaml_parse().

Both valid YAML controls are checked three ways against the hand-written typed trees in
controls/yaml/check_controls.py: the LLVM-coverage base image (which records yaml.c/parse.c/detect.c and libyaml
lines), and the AFL++-instrumented runtime running the full harness and the parse-only fuzz target. The AFL++
allowlist limits instrumentation to the extension's yaml.c, parse.c and detect.c and libyaml's reader.c,
scanner.c and parser.c; PHP is compiled with afl-clang-fast under an allowlist that matches no PHP source. The
build checks that exactly those six objects carry AFL++ edges, that the extension sources and licenses match the
manifest hashes, and that the reflected yaml_parse signature is the documented one. Each control is probed
REPEATS times through both targets; the gate requires repeatable maps that differ between the controls and full
harness maps equal to the fuzz-target maps (the PHP tree walk runs no instrumented code). The script writes the
overlay receipt and the cell feedback receipt data/php/yaml/pecl-yaml-feedback-differential.json.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[5]
OVERLAY = Path(__file__).resolve().parent
RELATIVE = OVERLAY.relative_to(ROOT / 'fuzzing/afl-native')
PROJECT = ROOT / 'projects' / RELATIVE
REPORT = ROOT / 'data/php/yaml/pecl-yaml-feedback-differential.json'
MANIFEST = json.loads((PROJECT / 'manifest.json').read_text())
IMAGE = f'parsarium-afl/{RELATIVE.parts[0]}-php-{RELATIVE.parts[2]}:local'
BASE_IMAGE = f'parsarium/{RELATIVE.parts[0]}-php-{RELATIVE.parts[2]}:local'
REPEATS = 5
MAP_SIZES: set[str] = set()
INSTRUMENTED_OBJECTS = [
    'pecl-yaml-2.3.0/.libs/detect.o',
    'pecl-yaml-2.3.0/.libs/parse.o',
    'pecl-yaml-2.3.0/.libs/yaml.o',
    'yaml-0.2.5/build/src/.libs/parser.o',
    'yaml-0.2.5/build/src/.libs/reader.o',
    'yaml-0.2.5/build/src/.libs/scanner.o',
]
FULL_TARGET = ['/opt/php/bin/php', '/work/harness.php', '/input/case']
PARSE_ONLY_TARGET = ['/opt/php/bin/php', '/work/fuzz-target.php', '/input/case']
API_SIGNATURE = 'yaml yaml_parse($input,$pos,$ndocs,array $callbacks):'
CHECKS = runpy.run_path(str(ROOT / 'controls/yaml/check_controls.py'))


def oracle(path: Path) -> dict:
    tree = CHECKS['EXPECTED'][path.name]
    return {**CHECKS['summary'](tree), 'tree': tree}


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
        raise RuntimeError('base pecl/yaml project must be verified first')
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
        if oracle(path) != expected[key]:
            raise RuntimeError(f'{key}: manifest tree differs from the YAML oracle')
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
        if run(['docker', 'run', '--rm', '--entrypoint', 'cat', image, '/work/yaml-sources.txt']) != extension_sources:
            raise RuntimeError(f'{image}: pecl/yaml sources differ from the manifest')
    runtime = run(['docker', 'run', '--rm', '--entrypoint', '/opt/php/bin/php', IMAGE, '-r',
                   'echo PHP_VERSION, " ", phpversion("yaml"), " ", implode(",", get_loaded_extensions());'])
    php_version, yaml_version, extensions = runtime.split(' ', 2)
    if (php_version, yaml_version) != ('8.5.12', '2.3.0') or 'yaml' not in extensions.split(','):
        raise RuntimeError(f'unexpected instrumented runtime: {runtime}')
    libyaml = run(['docker', 'run', '--rm', '--entrypoint', '/opt/php/bin/php', IMAGE, '--ri', 'yaml'])
    if not re.search(r'LibYAML Version => 0\.2\.5$', libyaml, re.M):
        raise RuntimeError(f'unexpected libyaml version: {libyaml}')
    signature = run(['docker', 'run', '--rm', '--entrypoint', '/opt/php/bin/php', IMAGE, '-r',
                     '$f = new ReflectionFunction("yaml_parse"); echo $f->getExtensionName(), " yaml_parse(", '
                     'implode(",", array_map(fn ($p) => ltrim($p->getType() . " $" . $p->getName()), '
                     '$f->getParameters())), "): ", $f->getReturnType();'])
    if signature != API_SIGNATURE:
        raise RuntimeError(f'unexpected yaml_parse signature: {signature}')
    instrumented = run(['docker', 'run', '--rm', '--entrypoint', 'cat', IMAGE,
                        '/work/afl-instrumented-objects.txt']).splitlines()
    if instrumented != INSTRUMENTED_OBJECTS:
        raise RuntimeError(f'AFL++ allowlist instrumented other objects: {instrumented}')
    for key, path in controls.items():
        output = json.loads(run([*sandbox(path), '--entrypoint', '/opt/php/bin/php', IMAGE,
                                 '/work/harness.php', '/input/case']))
        if json.dumps(output, ensure_ascii=False) != json.dumps(expected[key], ensure_ascii=False):
            raise RuntimeError(f'{key}: instrumented harness output differs from oracle: {output}')
    with tempfile.TemporaryDirectory(prefix='parsarium-pecl-yaml-afl-') as temporary:
        work = Path(temporary)
        coverage = {key: base_coverage(path, work / f'base-{key}') for key, path in controls.items()}
        full = {key: stable(path, work, f'full-{key}', FULL_TARGET) for key, path in controls.items()}
        parse = {key: stable(path, work, f'parse-{key}', PARSE_ONLY_TARGET) for key, path in controls.items()}
    for key in controls:
        if coverage[key]['output'] != expected[key]:
            raise RuntimeError(f'{key}: LLVM-coverage base output differs from oracle')
    for field in ('parser_source_lines_covered', 'underlying_source_lines_covered'):
        if coverage['control'][field] != base[field]:
            raise RuntimeError(f'base coverage replay differs from the project receipt: {field}')
    if len(MAP_SIZES) != 1:
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
        'underlying_source_lines_covered', 'underlying_parser_c_lines_covered',
        'underlying_scanner_c_lines_covered')}
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'native_libyaml_php_yaml_parser_source_edges',
        'feedback_scope': 'pecl/yaml 2.3.0 yaml.c (yaml_parse), parse.c (events to PHP values, aliases, tag '
                          'callbacks) and detect.c (implicit scalar typing) plus libyaml 0.2.5 reader.c, '
                          'scanner.c and parser.c via AFL++ allowlist; emit.c, libyaml api/loader/emitter code '
                          'and the PHP runtime are uninstrumented',
        'fuzz_target': 'projects/yaml/php/pecl_yaml/fuzz-target.php (yaml_parse with the YAML_MAP_TAG callback, '
                       'no tree walk or JSON output)',
        'harness': 'projects/yaml/php/pecl_yaml/harness.php (yaml_parse with the YAML_MAP_TAG callback, then the '
                   'typed-tree walk and JSON output)',
        'extension_source_sha256': MANIFEST['extension_source_sha256'],
        'api_signature': signature,
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'base_image_id': base_image_id,
        'source_sha256': MANIFEST['source_sha256'],
        'underlying_source_sha256': MANIFEST['underlying_source_sha256'],
        'php_source_sha256': MANIFEST['php_source_sha256'],
        'license_file_sha256': MANIFEST['license_file_sha256'],
        'runtime': {'php': php_version, 'pecl_yaml': yaml_version, 'libyaml': '0.2.5'},
        'instrumented_objects': instrumented,
        'control_sha256': MANIFEST['control_sha256'],
        'differential_control_sha256': MANIFEST['differential_control_sha256'],
        'oracle': 'controls/yaml/check_controls.py hand-written typed trees (cross-checked with Ruby Psych)',
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
        'full_harness_maps_equal_fuzz_target': True,
        'overlay_file_sha256': {
            name: sha256((OVERLAY / name).read_bytes()).hexdigest()
            for name in ('Dockerfile', 'build.py')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    report = {
        'project': str(RELATIVE), 'pass': True,
        'feedback_kind': receipt['feedback_kind'],
        'oracle': receipt['oracle'],
        'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
        'base_image_id': base_image_id, 'overlay_image_id': image_id,
        'release_source_sha256': MANIFEST['source_sha256'],
        'parser_source_prefix': MANIFEST['coverage_subject_prefix'],
        'underlying_source_prefix': MANIFEST['underlying_coverage_subject_prefix'],
        'control': MANIFEST['control'], 'control_sha256': MANIFEST['control_sha256'],
        'differential': MANIFEST['differential_control'],
        'differential_sha256': MANIFEST['differential_control_sha256'],
        'control_output_matches_oracle': True, 'differential_output_matches_oracle': True,
        'ordered_members_and_scalar_types_checked': True,
        'control_extension_lines_by_file': coverage['control']['extension_lines_by_file'],
        'differential_extension_lines_by_file': coverage['differential']['extension_lines_by_file'],
        'control_libyaml_lines_by_file': coverage['control']['underlying_lines_by_file'],
        'differential_libyaml_lines_by_file': coverage['differential']['underlying_lines_by_file'],
        'runs_per_control': REPEATS,
        'repeated_control_identical': True, 'repeated_differential_identical': True,
        'control_afl_tuples': len(parse['control']),
        'differential_afl_tuples': len(parse['differential']),
        'afl_tuple_difference': len(parse_difference),
        'full_harness_maps_equal_fuzz_target': True,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(f'Verified {RELATIVE}: {len(parse["control"])}/{len(parse["differential"])} fuzz-target tuples, '
          f'{len(parse_difference)} differ; full harness maps equal; {REPEATS} identical repeats per control')


if __name__ == '__main__':
    main()
