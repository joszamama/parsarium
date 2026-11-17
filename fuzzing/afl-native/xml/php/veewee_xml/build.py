"""Build and verify native libxml2 + PHP ext/dom AFL++ feedback for veewee/xml's xml_decode().

Both valid XML controls are checked three ways against an expat oracle computed here, independently of PHP
and libxml2: the Xdebug base image (which also records the veewee/xml lines each control executes), and the
AFL++-instrumented runtime running the same xml_decode harness. xml_decode returns qualified element and
attribute names plus every element's own xmlns declarations, so the oracle parses without namespace processing
and keeps those fields; a second check resolves the summary's declarations and compares the resulting expanded
names with expat in namespace mode. The AFL++ allowlist limits instrumentation to libxml2's XML parser sources
and the ext/dom sources that load a Dom\\XMLDocument from a string; the build checks that exactly those objects
carry AFL++ edges. Each control is probed REPEATS times through the full harness (xml_decode plus summary) and
through a bare Dom\\XMLDocument::createFromString with xml_decode's default options, so the input-dependent
tuples are shown to be repeatable and to arise while the document is loaded, not during veewee's tree walk.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from xml.parsers import expat


ROOT = Path(__file__).resolve().parents[5]
OVERLAY = Path(__file__).resolve().parent
RELATIVE = OVERLAY.relative_to(ROOT / 'fuzzing/afl-native')
PROJECT = ROOT / 'projects' / RELATIVE
MANIFEST = json.loads((PROJECT / 'manifest.json').read_text())
IMAGE = f'parsarium-afl/{RELATIVE.parts[0]}-php-{RELATIVE.parts[2]}:local'
BASE_IMAGE = f'parsarium/{RELATIVE.parts[0]}-php-{RELATIVE.parts[2]}:local'
REPEATS = 5
MAP_SIZES: set[str] = set()
PACKAGE_PREFIX = '/work/vendor/veewee/xml/src/'
INSTRUMENTED_OBJECTS = [
    'libxml2-2.15.4/build/.libs/libxml2_la-SAX2.o',
    'libxml2-2.15.4/build/.libs/libxml2_la-parser.o',
    'libxml2-2.15.4/build/.libs/libxml2_la-parserInternals.o',
    'php-8.5.12/ext/dom/document.o',
    'php-8.5.12/ext/dom/xml_document.o',
]
FULL_TARGET = ['/opt/php/bin/php', '/work/fuzz-target.php', '/input/case']
PARSE_ONLY_TARGET = ['/opt/php/bin/php', '-r',
                     'Dom\\XMLDocument::createFromString(file_get_contents($argv[1]));', '/input/case']


def oracle(data: bytes) -> dict:
    """Expat summary of the fields xml_decode exposes: qualified element names, non-declaration attributes,
    each element's own xmlns declarations, and the trimmed text of elements without child elements."""
    parser = expat.ParserCreate('UTF-8')
    parser.ordered_attributes = True
    state = {'elements': [], 'attributes': [], 'namespaces': [], 'max_depth': 0, 'segments': []}
    stack: list[dict] = []

    def start(name, attributes):
        if stack:
            stack[-1]['has_children'] = True
        stack.append({'text': [], 'has_children': False})
        state['max_depth'] = max(state['max_depth'], len(stack))
        state['elements'].append(name)
        for key, value in zip(attributes[::2], attributes[1::2]):
            if key == 'xmlns' or key.startswith('xmlns:'):
                state['namespaces'].append(f"{len(state['elements']) - 1} {name} {key}={value}")
            else:
                state['attributes'].append(f'{key}={value}')

    def end(_name):
        element = stack.pop()
        segment = ''.join(element['text']).strip(' \t\n\r')
        if not element['has_children'] and segment:
            state['segments'].append(segment)

    def text(value):
        if stack:
            stack[-1]['text'].append(value)

    parser.StartElementHandler, parser.EndElementHandler = start, end
    parser.CharacterDataHandler = text
    parser.Parse(data, True)
    return {'attributes': state['attributes'], 'elements': state['elements'],
            'max_depth': state['max_depth'], 'namespace_declarations': state['namespaces'],
            'root': state['elements'][0], 'text': state['segments']}


def expanded_names(data: bytes) -> list[str]:
    """Clark-notation element names from expat with namespace processing."""
    parser = expat.ParserCreate('UTF-8', '}')
    names: list[str] = []
    parser.StartElementHandler = lambda name, _attributes: names.append('{' + name if '}' in name else name)
    parser.Parse(data, True)
    return names


def resolve_summary(summary: dict, data: bytes) -> list[str]:
    """Resolve the summary's qualified element names through its indexed per-element declarations, using the
    document's nesting (the summary lists elements in document order) for scope."""
    declared: dict[int, dict[str, str]] = {}
    for entry in summary['namespace_declarations']:
        index, _element, declaration = entry.split(' ', 2)
        key, uri = declaration.split('=', 1)
        declared.setdefault(int(index), {})[key.removeprefix('xmlns').removeprefix(':')] = uri
    parser = expat.ParserCreate('UTF-8')
    scopes: list[dict[str, str]] = [{}]
    resolved: list[str] = []

    def start(name, _attributes):
        index = len(resolved)
        qualified = summary['elements'][index]
        if qualified != name:
            raise RuntimeError(f'summary element {index} is {qualified}, document has {name}')
        scopes.append({**scopes[-1], **declared.get(index, {})})
        prefix, _, local = qualified.rpartition(':')
        uri = scopes[-1].get(prefix, '')
        resolved.append(f'{{{uri}}}{local}' if uri else local)

    parser.StartElementHandler = start
    parser.EndElementHandler = lambda _name: scopes.pop()
    parser.Parse(data, True)
    return resolved


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
    """Replay one control in the Xdebug base image twice; return its summary and veewee/xml lines per file."""
    replays = []
    for index in range(2):
        out = work / str(index)
        out.mkdir(parents=True)
        run([*sandbox(case, out, '/input/control'), BASE_IMAGE])
        summary = json.loads((out / 'summary.json').read_text())
        files = json.loads((out / 'coverage.json').read_text())['data'][0]['files']
        summary['files'] = {f['filename'].removeprefix(PACKAGE_PREFIX): f['executed_lines'] for f in files}
        replays.append(summary)
    if replays[0] != replays[1]:
        raise RuntimeError(f'{case.name}: repeated Xdebug replays differ')
    return replays[0]


def line_set(files: dict[str, list[int]]) -> set[str]:
    return {f'{name}:{line}' for name, lines in files.items() for line in lines}


def main() -> None:
    base_receipt = PROJECT / 'verification.json'
    if not base_receipt.is_file() or not json.loads(base_receipt.read_text()).get('pass'):
        raise RuntimeError('base PHP project must be verified first')
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
    target = json.loads((PROJECT / 'target.json').read_text())['expected_by_control_sha256']
    for key, path in controls.items():
        data = path.read_bytes()
        if oracle(data) != expected[key] or target[digests[key]] != expected[key]:
            raise RuntimeError(f'{key}: manifest or target output differs from the expat oracle')
        if resolve_summary(expected[key], data) != expanded_names(data):
            raise RuntimeError(f'{key}: declarations do not resolve to the namespace-aware expat names')
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
    runtime = run(['docker', 'run', '--rm', '--entrypoint', '/opt/php/bin/php', IMAGE, '-r',
                   'echo PHP_VERSION, " ", LIBXML_DOTTED_VERSION, " ", implode(",", get_loaded_extensions());'])
    php_version, libxml_version, extensions = runtime.split(' ', 2)
    if (php_version, libxml_version) != ('8.5.12', '2.15.4') or 'dom' not in extensions.split(','):
        raise RuntimeError(f'unexpected instrumented runtime: {runtime}')
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
    with tempfile.TemporaryDirectory(prefix='parsarium-php-veewee-afl-') as temporary:
        work = Path(temporary)
        coverage = {key: base_coverage(path, work / f'base-{key}') for key, path in controls.items()}
        full = {key: stable(path, work, f'full-{key}', FULL_TARGET) for key, path in controls.items()}
        parse = {key: stable(path, work, f'parse-{key}', PARSE_ONLY_TARGET) for key, path in controls.items()}
    for key in controls:
        if coverage[key]['output'] != expected[key]:
            raise RuntimeError(f'{key}: Xdebug base output differs from oracle')
    if coverage['control']['parser_source_lines_covered'] != base['parser_source_lines_covered']:
        raise RuntimeError('base coverage replay differs from the project receipt')
    # Both controls take the same xml_decode branches, so the Xdebug line sets may be identical; the receipt
    # records that instead of requiring a difference.
    lines = {key: line_set(coverage[key]['files']) for key in controls}
    if len(MAP_SIZES) != 1:
        raise RuntimeError(f'afl-showmap map sizes: {MAP_SIZES}')
    full_edges = {key: edges(value) for key, value in full.items()}
    parse_edges = {key: edges(value) for key, value in parse.items()}
    full_difference = full_edges['control'] ^ full_edges['differential']
    parse_difference = parse_edges['control'] ^ parse_edges['differential']
    post_parse = {key: full_edges[key] - parse_edges[key] for key in controls}
    parse_attributed = full_difference & parse_difference
    traversal_only = full_difference - parse_difference
    if not parse_attributed or traversal_only or post_parse['control'] != post_parse['differential']:
        raise RuntimeError(f'input-dependent tuples are not isolated to loading: {len(parse_attributed)} '
                           f'load-time, {len(traversal_only)} only with xml_decode/summary')
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'native_libxml2_php_dom_parser_source_edges',
        'feedback_scope': 'libxml2 2.15.4 parser.c, parserInternals.c and SAX2.c plus PHP 8.5.12 '
                          'ext/dom/xml_document.c and document.c (Dom\\XMLDocument::createFromString) via AFL++ '
                          'allowlist; libxml2 tree, XPath and dict code, ext/dom/namespace_compat.c and the other '
                          'ext/dom sources, ext/libxml/libxml.c, the Zend engine and the interpreted veewee/xml '
                          'and php-standard-library PHP code are uninstrumented',
        'harness': 'projects/xml/php/veewee_xml/fuzz-target.php -> harness.php parsarium_parse '
                   '(VeeWee\\Xml\\Encoding\\xml_decode($bytes), summary.php array walk)',
        'parse_only_target': 'Dom\\XMLDocument::createFromString with options 0, the call veewee/xml\'s '
                             'xml_string_loader makes for xml_decode',
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'base_image_id': base_image_id,
        'source_sha256': MANIFEST['source_sha256'],
        'underlying_source_sha256': MANIFEST['underlying_source_sha256'],
        'php_source_sha256': MANIFEST['php_source_sha256'],
        'runtime': {'php': php_version, 'libxml2': libxml_version},
        'instrumented_objects': instrumented,
        'control_sha256': MANIFEST['control_sha256'],
        'differential_control_sha256': MANIFEST['differential_control_sha256'],
        'oracle': 'fuzzing/afl-native/xml/php/veewee_xml/build.py oracle(): expat without namespace '
                  'processing, fields exposed by xml_decode; resolve_summary() checks the declarations '
                  'against expat with namespace processing',
        'control_output_matches_oracle': True,
        'differential_output_matches_oracle': True,
        'declarations_resolve_to_expanded_names': True,
        'package_line_coverage': {
            'tool': 'Xdebug (Ubuntu PHP 8.5.4, libxml 2.15.2), two identical replays per control',
            'subject': 'vendor/veewee/xml/src/',
            'control_lines': len(lines['control']),
            'differential_lines': len(lines['differential']),
            'shared_lines': len(lines['control'] & lines['differential']),
            'control_only_lines': sorted(lines['control'] - lines['differential']),
            'differential_only_lines': sorted(lines['differential'] - lines['control']),
            'line_sets_identical': lines['control'] == lines['differential'],
            'encoding_lines': {key: coverage[key]['encoding_source_lines_covered'] for key in controls},
            'files': {key: sorted(coverage[key]['files']) for key in controls},
        },
        'image_id': image_id, 'platform': MANIFEST['platform'],
        'afl_package': version, 'afl_map_size': int(next(iter(MAP_SIZES))),
        'repeats_per_control': REPEATS,
        'all_repeats_identical': True,
        'feedback_edges': len(full['control']),
        'differential_feedback_edges': len(full['differential']),
        'stable_shared_edges': len(full_edges['control'] & full_edges['differential']),
        'stable_control_only_edges': len(full_edges['control'] - full_edges['differential']),
        'stable_differential_only_edges': len(full_edges['differential'] - full_edges['control']),
        'afl_tuple_difference': len(full_difference),
        'parse_only_control_edges': len(parse['control']),
        'parse_only_differential_edges': len(parse['differential']),
        'parse_only_tuple_difference': len(parse_difference),
        'format_dependent_parse_time_tuples': len(parse_attributed),
        'format_dependent_traversal_only_tuples': len(traversal_only),
        'post_parse_control_edges': len(post_parse['control']),
        'post_parse_differential_edges': len(post_parse['differential']),
        'post_parse_edges_identical': True,
        'overlay_file_sha256': {
            name: sha256((OVERLAY / name).read_bytes()).hexdigest()
            for name in ('Dockerfile', 'build.py')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: veewee/xml {len(lines["control"])}/{len(lines["differential"])} lines '
          f'({len(lines["control"] ^ lines["differential"])} differ); {len(full["control"])}/'
          f'{len(full["differential"])} native parser tuples, {len(full_difference)} differ '
          f'({len(parse_attributed)} load-time); {REPEATS} identical repeats per control')


if __name__ == '__main__':
    main()
