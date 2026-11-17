"""Check xmlschema.XMLResource against an lxml oracle and its ElementTree/Expat feedback on two fixed, valid XML controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/xml/python/xmlschema'
OVERLAY = ROOT / 'fuzzing/afl-native/xml/python/xmlschema'
LXML = ROOT / 'projects/xml/python/lxml'
REPORT = ROOT / 'data/python/xml/xmlschema-valid-feedback.json'
PACKAGES = '/opt/venv/lib/python3.14/site-packages/'
XMLSCHEMA = PACKAGES + 'xmlschema/'
DRIVER = '/usr/lib/python3.14/xml/etree/'
EXPAT = '/work/expat/lib/'
REQUIRED = (XMLSCHEMA + 'resources/xml_resource.py:', XMLSCHEMA + 'resources/xml_loader.py:',
            DRIVER + 'ElementTree.py:', EXPAT + 'xmlparse.c:')
REPEATS = 5

# Namespace-aware libxml2 oracle, run in the verified lxml image. It reports the
# lxml path's full summary (including the xmlns declaration count) and each
# element's in-scope namespace map in document order, with None as ''.
ORACLE = r'''
import json, sys
from lxml import etree

parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=False)
root = etree.parse(sys.argv[1], parser).getroot()
state = {"attributes": [], "elements": [], "max_depth": 0,
         "namespace_declarations": 0, "namespaces": set(), "text": []}
nsmaps = []

def text(value):
    if value and value.strip():
        state["text"].append(value.strip())

def walk(element, depth, inherited):
    state["elements"].append(element.tag)
    state["max_depth"] = max(state["max_depth"], depth)
    current = element.nsmap
    nsmaps.append({prefix or "": uri for prefix, uri in current.items()})
    for prefix, uri in current.items():
        if inherited.get(prefix) != uri:
            state["namespace_declarations"] += 1
            if uri:
                state["namespaces"].add(uri)
    for key, value in element.attrib.items():
        state["attributes"].append(key + "=" + value)
    text(element.text)
    for child in element:
        if isinstance(child.tag, str):
            walk(child, depth + 1, current)
        text(child.tail)

walk(root, 1, {})
state["namespaces"] = sorted(state["namespaces"])
state["root"] = root.tag
print(json.dumps({"summary": state, "nsmaps": nsmaps}, ensure_ascii=False))
'''

# xmlschema's own namespace bookkeeping, read from the same resource: per-element
# in-scope maps (get_nsmap) in document order and the documented merged map.
NSMAPS = r'''
import json, sys
from pathlib import Path
from harness import parse_resource

resource = parse_resource(Path(sys.argv[1]).read_bytes())
print(json.dumps({"nsmaps": [resource.get_nsmap(element) for element in resource.root.iter()],
                  "get_namespaces_all": resource.get_namespaces(root_only=False)}, ensure_ascii=False))
'''

PARSER_CHECK = ('import _elementtree, pyexpat, xml.etree.ElementTree as et; from io import BytesIO; '
                'from xmlschema import XMLResource; from xmlschema.resources.xml_loader import XMLResourceLoader; '
                'r = XMLResource(BytesIO(open("/input/case", "rb").read())); '
                'print(type(r).__module__ + "." + type(r).__name__, '
                'type(r).__mro__[1].__module__ + "." + type(r).__mro__[1].__name__, '
                'r._iterparse is et.iterparse, et.XMLParser is _elementtree.XMLParser and et.TreeBuilder is _elementtree.TreeBuilder, '
                'r.url is None and r.fp is None and not r.is_defused() and not r.is_lazy(), pyexpat.EXPAT_VERSION)')


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])
    return result.stdout


def sandbox(source: Path, scratch: Path) -> list[str]:
    return ['docker', 'run', '--rm', '--platform', 'linux/arm64', '--network', 'none',
            '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
            '--user', f'{os.getuid()}:{os.getgid()}', '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
            '-v', f'{source}:/input/case:ro', '-v', f'{scratch}:/coverage']


def probe(image: str, source: Path, scratch: Path, label: str) -> tuple[set[str], set[str]]:
    base = sandbox(source, scratch)
    run([*base, '--entrypoint', '/bin/sh', image,
         '/work/afl_trace', '/input/case', f'/coverage/{label}.features'])
    run([*base, '-e', 'AFL_MAP_SIZE=65536', '--entrypoint', 'afl-showmap', image,
         '-m', 'none', '-t', '120000', '-o', f'/coverage/{label}.map',
         '--', '/work/afl_proxy', '/input/case'])
    features = set((scratch / f'{label}.features').read_text().splitlines()) - {''}
    tuples = {line.split(':', 1)[0] for line in
              (scratch / f'{label}.map').read_text().splitlines() if line}
    if not features or not tuples or any(not value.startswith((PACKAGES, DRIVER, EXPAT)) for value in features):
        raise RuntimeError('feedback is empty or outside xmlschema/ElementTree driver/Expat source')
    for required in REQUIRED:
        if not any(value.startswith(required) for value in features):
            raise RuntimeError(f'{required} has no feedback')
    return features, tuples


def split(features: set[str]) -> tuple[set[str], set[str], set[str]]:
    return ({value for value in features if value.startswith(PACKAGES)},
            {value for value in features if value.startswith(DRIVER)},
            {value for value in features if value.startswith(EXPAT)})


def lines(features: set[str]) -> set[str]:
    """Python line features without their hit-count bucket."""
    return {value.rpartition('#')[0] for value in features}


def main() -> None:
    manifest = json.loads((PROJECT / 'manifest.json').read_text())
    base = json.loads((PROJECT / 'verification.json').read_text())
    overlay = json.loads((OVERLAY / 'verification.json').read_text())
    lxml_manifest = json.loads((LXML / 'manifest.json').read_text())
    lxml_image = json.loads((LXML / 'verification.json').read_text())['image_id']
    if overlay['base_image_id'] != base['image_id']:
        raise RuntimeError('AFL overlay base differs from verified project')
    if overlay['base_project_receipt_sha256'] != sha256((PROJECT / 'verification.json').read_bytes()).hexdigest():
        raise RuntimeError('AFL overlay was built from a different project receipt')
    controls = (('control', manifest['control'], manifest['control_sha256'], 'expected_output'),
                ('variant', manifest['differential_control'], manifest['differential_control_sha256'],
                 'differential_expected_output'))
    for _, path, digest, _ in controls:
        if sha256((ROOT / path).read_bytes()).hexdigest() != digest:
            raise RuntimeError('valid control hash changed')
    if (lxml_manifest['control'], lxml_manifest['differential_control']) != (
            manifest['control'], manifest['differential_control']):
        raise RuntimeError('lxml oracle uses different controls')
    with tempfile.TemporaryDirectory(prefix='parsarium-xmlschema-feedback-') as temporary:
        scratch = Path(temporary)
        outputs, oracle, namespaces = {}, {}, {}
        for name, path, _, key in controls:
            source = ROOT / path
            outputs[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                            '/opt/venv/bin/python', base['image_id'],
                                            '/work/replay.py', '/input/case']))
            if outputs[name] != manifest[key]:
                raise RuntimeError(f'{name} xmlschema summary changed: {outputs[name]}')
            oracle[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                           '/opt/venv/bin/python', lxml_image,
                                           '-c', ORACLE, '/input/case']))
            if oracle[name]['summary'] != lxml_manifest[key]:
                raise RuntimeError(f'{name} oracle differs from the verified lxml path')
            if oracle[name]['summary'] != outputs[name]:
                raise RuntimeError(f'{name} xmlschema summary differs from the oracle: {oracle[name]["summary"]}')
            namespaces[name] = json.loads(run([*sandbox(source, scratch), '-w', '/work', '--entrypoint',
                                               '/opt/venv/bin/python', base['image_id'],
                                               '-c', NSMAPS, '/input/case']))
            if namespaces[name]['nsmaps'] != oracle[name]['nsmaps']:
                raise RuntimeError(f'{name} xmlschema in-scope namespace maps differ from lxml: {namespaces[name]}')
            declared = sorted(uri for uri in namespaces[name]['get_namespaces_all'].values() if uri)
            if declared != outputs[name]['namespaces']:
                raise RuntimeError(f'{name} get_namespaces(root_only=False) URIs differ: {declared}')
        checked = run([*sandbox(ROOT / manifest['control'], scratch), '--entrypoint',
                       '/opt/venv/bin/python', base['image_id'], '-c', PARSER_CHECK]).split()
        if checked != ['xmlschema.resources.xml_resource.XMLResource',
                       'xmlschema.resources.xml_loader.XMLResourceLoader',
                       'True', 'True', 'True', 'expat_2.10.0']:
            raise RuntimeError(f'resource class, iterparse, C parser or source handling changed: {checked}')
        runs_a = [probe(overlay['image_id'], ROOT / manifest['control'], scratch, f'control-{index}')
                  for index in range(REPEATS)]
        runs_b = [probe(overlay['image_id'], ROOT / manifest['differential_control'], scratch, f'variant-{index}')
                  for index in range(REPEATS)]
    first, other = runs_a[0], runs_b[0]
    if any(item != first for item in runs_a[1:]) or any(item != other for item in runs_b[1:]):
        raise RuntimeError('repeated xmlschema/Expat source feedback is unstable')
    (py_a, et_a, expat_a), (py_b, et_b, expat_b) = split(first[0]), split(other[0])
    feature_diff = len(first[0] ^ other[0])
    tuple_diff = len(first[1] ^ other[1])
    if feature_diff == 0 or tuple_diff == 0 or not expat_a ^ expat_b or not py_a ^ py_b:
        raise RuntimeError('xmlschema or Expat feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    changed_package_lines = sorted({value.rpartition('#')[0].removeprefix(PACKAGES) for value in py_a ^ py_b})
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'xml/python/xmlschema', 'pass': True,
              'input_kind': 'two fixed valid UTF-8 XML 1.0 namespace controls without DOCTYPE',
              'tested_resource': checked[0], 'tested_resource_base': checked[1],
              'iterparse': 'xml.etree.ElementTree.iterparse (default; pure-Python iterparse/XMLPullParser driver)',
              'xml_parser_and_tree_builder': '_elementtree.XMLParser and _elementtree.TreeBuilder (C accelerator, not covered)',
              'source_handling': 'BytesIO source: no URL, no file object, not defused, not lazy',
              'expat_version': checked[5],
              'oracle': 'lxml 6.1.3 / libxml2 2.15.4 namespace-aware parse in the verified lxml image; '
                        'full lxml-path summary including the xmlns declaration count, plus per-element nsmap',
              'oracle_image_id': lxml_image,
              'oracle_matches_lxml_path': True,
              'xmlschema_matches_oracle': True,
              'xmlschema_nsmaps_match_lxml_nsmaps': True,
              'get_namespaces_uris_equal_declared_uris': True,
              'control_nsmaps': namespaces['control']['nsmaps'],
              'variant_nsmaps': namespaces['variant']['nsmaps'],
              'feedback_scope': 'executed Python lines (each tagged with its AFL++ hit-count bucket) of xmlschema 4.3.2 '
                                'and CPython 3.14 xml/etree during the XMLResource(BytesIO(data)) call, plus Expat 2.10.0 '
                                'LLVM regions and branches under /work/expat/lib; harness and post-parse summary lines are excluded',
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'],
              'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'repeated_control_runs': REPEATS, 'control_repeat_identical': True,
              'repeated_variant_runs': REPEATS, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'control_package_features': len(py_a), 'variant_package_features': len(py_b),
              'control_elementtree_driver_features': len(et_a), 'variant_elementtree_driver_features': len(et_b),
              'control_expat_features': len(expat_a), 'variant_expat_features': len(expat_b),
              'parser_feature_difference': feature_diff,
              'package_feature_difference': len(py_a ^ py_b),
              'package_line_set_difference': len(lines(py_a) ^ lines(py_b)),
              'package_lines_with_changed_hit_bucket': changed_package_lines,
              'elementtree_driver_feature_difference': len(et_a ^ et_b),
              'elementtree_driver_line_set_difference': len(lines(et_a) ^ lines(et_b)),
              'expat_feature_difference': len(expat_a ^ expat_b),
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
