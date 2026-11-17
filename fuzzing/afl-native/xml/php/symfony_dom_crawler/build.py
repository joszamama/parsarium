"""Build and verify native libxml2 + PHP ext/dom AFL++ feedback for symfony/dom-crawler.

The instrumented PHP 8.5.12 runtime runs the same Crawler::addXmlContent harness as the base project on
both valid XML controls. Its output must equal an expat oracle computed here, independently of PHP and
libxml2. The AFL++ allowlist limits instrumentation to libxml2's XML parser sources and to PHP's
DOMDocument loading and libxml glue; the build checks that exactly those objects carry AFL++ edges.
Each control is probed REPEATS times through the full harness and through addXmlContent alone, so the
format-dependent tuples are shown to be repeatable and to arise while libxml2 parses the text, not
during Crawler's later navigation.
"""

from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from xml.parsers import expat


ROOT = Path(__file__).resolve().parents[5]
OVERLAY = Path(__file__).resolve().parent
RELATIVE = OVERLAY.relative_to(ROOT / 'fuzzing/afl-native')
PROJECT = ROOT / 'projects' / RELATIVE
MANIFEST = json.loads((PROJECT / 'manifest.json').read_text())
IMAGE = f'parsarium-afl/{RELATIVE.parts[0]}-php-{RELATIVE.parts[2]}:local'
REPEATS = 5
MAP_SIZES: set[str] = set()
INSTRUMENTED_OBJECTS = [
    'libxml2-2.15.4/build/.libs/libxml2_la-SAX2.o',
    'libxml2-2.15.4/build/.libs/libxml2_la-parser.o',
    'libxml2-2.15.4/build/.libs/libxml2_la-parserInternals.o',
    'php-8.5.12/ext/dom/document.o',
    'php-8.5.12/ext/libxml/libxml.o',
]
FULL_TARGET = ['/opt/php/bin/php', '/work/fuzz-target.php', '/input/case']
PARSE_ONLY_TARGET = ['/opt/php/bin/php', '-r',
                     'require "/work/autoload.php"; (new Symfony\\Component\\DomCrawler\\Crawler())'
                     '->addXmlContent(file_get_contents($argv[1]));', '/input/case']

sys.path.insert(0, str(ROOT / 'controls/xml'))
from check_controls import summarize  # noqa: E402


def run(command: list[str], with_log: bool = False) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'{command[:5]} failed: {(result.stdout + result.stderr)[-3000:]}')
    return (result.stdout + result.stderr) if with_log else result.stdout.strip()


def sandbox(case: Path, work: Path | None = None) -> list[str]:
    command = ['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
               '--network', 'none', '--read-only', '--cap-drop', 'ALL',
               '--security-opt', 'no-new-privileges',
               '--user', f'{os.getuid()}:{os.getgid()}',
               '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
               '-v', f'{case}:/input/case:ro']
    return command + (['-v', f'{work}:/coverage'] if work else [])


def oracle(data: bytes) -> dict:
    """Expat summary plus the Crawler xpath counts expected from the harness naming rule."""
    expected = summarize(data)
    expected = {key: expected[key] for key in ('attributes', 'elements', 'max_depth', 'root', 'text')}
    parser = expat.ParserCreate('UTF-8', ' ')
    parser.namespace_prefixes = True
    names, defaults = [], {}

    def start(name, _attributes):
        uri, local, prefix = (name.split(' ') + ['', ''])[:3] if ' ' in name else ('', name, '')
        if prefix:
            key = f'//{prefix}:{local}'
        elif uri:
            key = f'//{defaults.setdefault(uri, f"ns{len(defaults) + 1}")}:{local}'
        else:
            key = f'//{local}'
        names.append((key, uri, local))

    parser.StartElementHandler = start
    parser.Parse(data, True)
    counts = Counter((uri, local) for _, uri, local in names)
    expected['xpath'] = {key: counts[(uri, local)] for key, uri, local in names}
    return expected


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


def main() -> None:
    base_receipt = PROJECT / 'verification.json'
    if not base_receipt.is_file() or not json.loads(base_receipt.read_text()).get('pass'):
        raise RuntimeError('base PHP runtime project must be verified first')
    controls = {'control': ROOT / MANIFEST['control'],
                'differential': ROOT / MANIFEST['differential_control']}
    digests = {'control': MANIFEST['control_sha256'],
               'differential': MANIFEST['differential_control_sha256']}
    for key, path in controls.items():
        if sha256(path.read_bytes()).hexdigest() != digests[key]:
            raise RuntimeError(f'{path} changed')
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
    expected = {'control': MANIFEST['expected_output'],
                'differential': MANIFEST['differential_expected_output']}
    outputs = {}
    for key, path in controls.items():
        independent = oracle(path.read_bytes())
        if independent != expected[key]:
            raise RuntimeError(f'{key}: manifest output differs from the expat oracle: {independent}')
        outputs[key] = json.loads(run([*sandbox(path), '--entrypoint', '/opt/php/bin/php', IMAGE,
                                       '/work/harness.php', '/input/case']))
        if outputs[key] != independent:
            raise RuntimeError(f'{key}: instrumented harness output differs from oracle: {outputs[key]}')
    with tempfile.TemporaryDirectory(prefix='parsarium-php-native-afl-') as temporary:
        work = Path(temporary)
        full = {key: stable(path, work, f'full-{key}', FULL_TARGET) for key, path in controls.items()}
        parse = {key: stable(path, work, f'parse-{key}', PARSE_ONLY_TARGET) for key, path in controls.items()}
    if len(MAP_SIZES) != 1:
        raise RuntimeError(f'afl-showmap map sizes: {MAP_SIZES}')
    full_edges = {key: edges(value) for key, value in full.items()}
    parse_edges = {key: edges(value) for key, value in parse.items()}
    full_difference = full_edges['control'] ^ full_edges['differential']
    parse_difference = parse_edges['control'] ^ parse_edges['differential']
    post_parse = {key: full_edges[key] - parse_edges[key] for key in controls}
    parse_attributed = full_difference & parse_difference
    navigation_only = full_difference - parse_difference
    if not parse_attributed or len(parse_attributed) < len(navigation_only):
        raise RuntimeError(f'format-dependent tuples are not parse-time: {len(parse_attributed)} '
                           f'parse-time, {len(navigation_only)} only after addXmlContent')
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'native_libxml2_php_dom_parser_source_edges',
        'feedback_scope': 'libxml2 2.15.4 parser.c, parserInternals.c and SAX2.c plus PHP 8.5.12 '
                          'ext/dom/document.c (DOMDocument::loadXML) and ext/libxml/libxml.c via AFL++ '
                          'allowlist; libxml2 tree, XPath and dict code, the other ext/dom classes, the Zend '
                          'engine and the interpreted Crawler PHP code are uninstrumented',
        'harness': 'projects/xml/php/symfony_dom_crawler/fuzz-target.php -> harness.php parsarium_parse '
                   '(new Crawler(), addXmlContent, summary traversal and filterXPath)',
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'source_sha256': MANIFEST['source_sha256'],
        'underlying_source_sha256': MANIFEST['underlying_source_sha256'],
        'php_source_sha256': MANIFEST['php_source_sha256'],
        'runtime': {'php': php_version, 'libxml2': libxml_version},
        'instrumented_objects': instrumented,
        'control_sha256': MANIFEST['control_sha256'],
        'differential_control_sha256': MANIFEST['differential_control_sha256'],
        'oracle': 'controls/xml/check_controls.py expat summary plus expanded-name xpath counts',
        'control_output_matches_oracle': True,
        'differential_output_matches_oracle': True,
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
        'format_dependent_post_parse_tuples': len(navigation_only),
        'post_parse_control_edges': len(post_parse['control']),
        'post_parse_differential_edges': len(post_parse['differential']),
        'post_parse_edges_identical': post_parse['control'] == post_parse['differential'],
        'overlay_file_sha256': {
            name: sha256((OVERLAY / name).read_bytes()).hexdigest()
            for name in ('Dockerfile', 'build.py')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {len(full["control"])}/{len(full["differential"])} native parser tuples, '
          f'{len(full_difference)} differ ({len(parse_attributed)} parse-time), '
          f'{REPEATS} identical repeats per control')


if __name__ == '__main__':
    main()
