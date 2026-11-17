"""Build and verify native libxml2 + PHP ext/xmlreader/ext/dom AFL++ feedback for saloonphp/xml-wrangler.

The instrumented PHP 8.5.12 runtime runs the same XmlReader::fromString()->elements() harness as the base project
on both valid XML controls. Its output must equal the project's expat oracle, computed here independently of PHP
and libxml2. The AFL++ allowlist limits instrumentation to libxml2's XML parser and reader sources and to PHP's
XMLReader and DOMDocument loading; the build checks that exactly those objects carry AFL++ edges. Each control is
probed REPEATS times through three targets: the full harness, elements() alone, and the veewee/xml Reader pass
alone (XMLReader over the original bytes, including readOuterXml, without the DOM decode). The full harness and
elements() must give the same map, because the summary walk is interpreted PHP over Element objects, and the
Reader pass alone must already differ between the controls. The standalone Reader script reaches edges the full
harness does not (one, from tearing down its XMLReader differently); they must be the same for both controls.
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
    'libxml2-2.15.4/build/.libs/libxml2_la-xmlreader.o',
    'php-8.5.12/ext/dom/document.o',
    'php-8.5.12/ext/xmlreader/php_xmlreader.o',
]
FULL_TARGET = ['/opt/php/bin/php', '/work/fuzz-target.php', '/input/case']
PARSE_ONLY_TARGET = ['/opt/php/bin/php', '-r',
                     'require "/work/vendor/autoload.php"; '
                     'Saloon\\XmlWrangler\\XmlReader::fromString(file_get_contents($argv[1]))->elements();',
                     '/input/case']
READER_ONLY_TARGET = ['/opt/php/bin/php', '-r',
                      'require "/work/vendor/autoload.php"; '
                      'foreach (VeeWee\\Xml\\Reader\\Reader::fromXmlString(file_get_contents($argv[1]))'
                      '->provide(VeeWee\\Xml\\Reader\\Matcher\\document_element()) as $match) {}',
                      '/input/case']

sys.path.insert(0, str(PROJECT))
from oracle import summarize  # noqa: E402


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
    base = json.loads(base_receipt.read_text()) if base_receipt.is_file() else {}
    if not base.get('pass'):
        raise RuntimeError('base PHP runtime project must be verified first')
    if run(['docker', 'image', 'inspect', BASE_IMAGE, '--format', '{{.Id}}']) != base['image_id']:
        raise RuntimeError('local base image is not the verified project image; rerun run_project.py')
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
    if (php_version, libxml_version) != ('8.5.12', '2.15.4') or not {'dom', 'xmlreader'} <= set(extensions.split(',')):
        raise RuntimeError(f'unexpected instrumented runtime: {runtime}')
    instrumented = run(['docker', 'run', '--rm', '--entrypoint', 'cat', IMAGE,
                        '/work/afl-instrumented-objects.txt']).splitlines()
    if instrumented != INSTRUMENTED_OBJECTS:
        raise RuntimeError(f'AFL++ allowlist instrumented other objects: {instrumented}')
    expected = {'control': MANIFEST['expected_output'],
                'differential': MANIFEST['differential_expected_output']}
    for key, path in controls.items():
        independent = summarize(path.read_bytes())
        if independent != expected[key]:
            raise RuntimeError(f'{key}: manifest output differs from the expat oracle: {independent}')
        output = json.loads(run([*sandbox(path), '--entrypoint', '/opt/php/bin/php', IMAGE,
                                 '/work/harness.php', '/input/case']))
        if output != independent:
            raise RuntimeError(f'{key}: instrumented harness output differs from oracle: {output}')
    with tempfile.TemporaryDirectory(prefix='parsarium-php-native-afl-') as temporary:
        work = Path(temporary)
        full = {key: stable(path, work, f'full-{key}', FULL_TARGET) for key, path in controls.items()}
        parse = {key: stable(path, work, f'parse-{key}', PARSE_ONLY_TARGET) for key, path in controls.items()}
        reader = {key: stable(path, work, f'reader-{key}', READER_ONLY_TARGET) for key, path in controls.items()}
    if len(MAP_SIZES) != 1:
        raise RuntimeError(f'afl-showmap map sizes: {MAP_SIZES}')
    full_edges = {key: edges(value) for key, value in full.items()}
    reader_edges = {key: edges(value) for key, value in reader.items()}
    full_difference = full_edges['control'] ^ full_edges['differential']
    reader_difference = reader_edges['control'] ^ reader_edges['differential']
    if not full_difference:
        raise RuntimeError('the two valid controls give the same AFL++ edges')
    if any(full[key] != parse[key] for key in controls):
        raise RuntimeError('the summary walk changed the native AFL++ map after elements()')
    if not reader_difference:
        raise RuntimeError('the XMLReader pass alone does not differ between the controls')
    reader_extra = {key: reader_edges[key] - full_edges[key] for key in controls}
    if reader_extra['control'] != reader_extra['differential']:
        raise RuntimeError('XMLReader-pass edges outside the full harness depend on the control')
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'native_libxml2_php_xmlreader_dom_parser_source_edges',
        'feedback_scope': 'libxml2 2.15.4 parser.c, parserInternals.c, SAX2.c and xmlreader.c plus PHP 8.5.12 '
                          'ext/xmlreader/php_xmlreader.c (XMLReader) and ext/dom/document.c (DOMDocument::loadXML) '
                          'via AFL++ allowlist; libxml2 tree, save, XPath and dict code, ext/libxml, the other '
                          'ext/dom classes, ext/sodium, the Zend engine and the interpreted XML Wrangler, veewee/xml '
                          'and php-standard-library PHP code are uninstrumented',
        'harness': 'projects/xml/php/saloon_xml_wrangler/fuzz-target.php -> harness.php parsarium_parse '
                   '(XmlReader::fromString, elements(), Element summary walk)',
        'shared_family': 'libxml2 via PHP XMLReader and DOMDocument, shared with the standard XMLReader and '
                         'DOMDocument paths, sabre/xml and symfony/dom-crawler',
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'base_image_id': base['image_id'],
        'source_sha256': MANIFEST['source_sha256'],
        'underlying_package_source_sha256': MANIFEST['underlying_package_source_sha256'],
        'underlying_source_sha256': MANIFEST['underlying_source_sha256'],
        'php_source_sha256': MANIFEST['php_source_sha256'],
        'runtime': {'php': php_version, 'libxml2': libxml_version, 'extensions': extensions.split(',')},
        'instrumented_objects': instrumented,
        'control_sha256': MANIFEST['control_sha256'],
        'differential_control_sha256': MANIFEST['differential_control_sha256'],
        'oracle': 'projects/xml/php/saloon_xml_wrangler/oracle.py (expat without namespace processing)',
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
        'elements_only_maps_equal_full_harness': True,
        'post_elements_edges': 0,
        'reader_pass_control_edges': len(reader['control']),
        'reader_pass_differential_edges': len(reader['differential']),
        'reader_pass_tuple_difference': len(reader_difference),
        'reader_pass_edges_outside_full_harness': len(reader_extra['control']),
        'reader_pass_edges_outside_full_harness_identical': True,
        'decode_pass_only_control_edges': len(full_edges['control'] - reader_edges['control']),
        'decode_pass_only_differential_edges': len(full_edges['differential'] - reader_edges['differential']),
        'overlay_file_sha256': {
            name: sha256((OVERLAY / name).read_bytes()).hexdigest()
            for name in ('Dockerfile', 'build.py')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {len(full["control"])}/{len(full["differential"])} native parser tuples, '
          f'{len(full_difference)} differ ({len(reader_difference)} in the XMLReader pass alone), '
          f'{REPEATS} identical repeats per control')


if __name__ == '__main__':
    main()
