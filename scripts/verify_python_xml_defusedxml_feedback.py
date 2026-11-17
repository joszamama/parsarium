"""Check defusedxml.ElementTree against an lxml oracle and its ElementTree/Expat feedback on two fixed, valid XML controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/xml/python/defusedxml'
OVERLAY = ROOT / 'fuzzing/afl-native/xml/python/defusedxml'
LXML = ROOT / 'projects/xml/python/lxml'
REPORT = ROOT / 'data/python/xml/defusedxml-valid-feedback.json'
PACKAGES = '/opt/venv/lib/python3.14/site-packages/'
DEFUSED = PACKAGES + 'defusedxml/'
DRIVER = '/usr/lib/python3.14/xml/etree/'
EXPAT = '/work/expat/lib/'
REQUIRED = (DEFUSED + 'ElementTree.py:', DEFUSED + 'common.py:', DRIVER + 'ElementTree.py:', EXPAT + 'xmlparse.c:')
REPEATS = 5

# Namespace-aware libxml2 oracle, run in the verified lxml image. It reports the
# lxml path's summary without the xmlns declaration count (ElementTree keeps no
# declarations), with namespaces taken from expanded names, and checks that this
# URI set equals the declared non-empty URIs on the control.
ORACLE = r'''
import json, sys
from lxml import etree

parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=False)
root = etree.parse(sys.argv[1], parser).getroot()
state = {"attributes": [], "elements": [], "max_depth": 0, "namespaces": set(), "text": []}
declared = set()

def uri(name):
    namespace = etree.QName(name).namespace
    if namespace:
        state["namespaces"].add(namespace)

def text(value):
    if value and value.strip():
        state["text"].append(value.strip())

def walk(element, depth, inherited):
    state["elements"].append(element.tag)
    uri(element.tag)
    state["max_depth"] = max(state["max_depth"], depth)
    for prefix, value in element.nsmap.items():
        if inherited.get(prefix) != value and value:
            declared.add(value)
    for key, value in element.attrib.items():
        uri(key)
        state["attributes"].append(key + "=" + value)
    text(element.text)
    for child in element:
        if isinstance(child.tag, str):
            walk(child, depth + 1, element.nsmap)
        text(child.tail)

walk(root, 1, {})
state["namespaces"] = sorted(state["namespaces"])
state["root"] = root.tag
print(json.dumps({"summary": state, "declared_namespaces": sorted(declared)}, ensure_ascii=False))
'''

PARSER_CHECK = ('import _elementtree, pyexpat, xml.etree.ElementTree as stdlib; import defusedxml.ElementTree as d; '
                'base = d.DefusedXMLParser.__mro__[1]; p = d.DefusedXMLParser(target=d._TreeBuilder()); '
                'print(type(p).__module__ + "." + type(p).__name__, base.__module__ + "." + base.__name__, '
                'base is not stdlib.XMLParser and hasattr(base, "_start"), d._TreeBuilder is _elementtree.TreeBuilder, '
                'p.parser.EntityDeclHandler == p.defused_entity_decl and '
                'p.parser.ExternalEntityRefHandler == p.defused_external_entity_ref_handler, pyexpat.EXPAT_VERSION)')


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
    if not features or not tuples or any(not value.startswith((DEFUSED, DRIVER, EXPAT)) for value in features):
        raise RuntimeError('feedback is empty or outside defusedxml/ElementTree driver/Expat source')
    for required in REQUIRED:
        if not any(value.startswith(required) for value in features):
            raise RuntimeError(f'{required} has no feedback')
    return features, tuples


def split(features: set[str]) -> tuple[set[str], set[str], set[str]]:
    return ({value for value in features if value.startswith(DEFUSED)},
            {value for value in features if value.startswith(DRIVER)},
            {value for value in features if value.startswith(EXPAT)})


def without_declarations(summary: dict) -> dict:
    return {key: value for key, value in summary.items() if key != 'namespace_declarations'}


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
    with tempfile.TemporaryDirectory(prefix='parsarium-defusedxml-feedback-') as temporary:
        scratch = Path(temporary)
        outputs, oracle = {}, {}
        for name, path, _, key in controls:
            source = ROOT / path
            outputs[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                            '/opt/venv/bin/python', base['image_id'],
                                            '/work/replay.py', '/input/case']))
            if outputs[name] != manifest[key]:
                raise RuntimeError(f'{name} defusedxml summary changed: {outputs[name]}')
            oracle[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                           '/opt/venv/bin/python', lxml_image,
                                           '-c', ORACLE, '/input/case']))
            if oracle[name]['summary'] != without_declarations(lxml_manifest[key]):
                raise RuntimeError(f'{name} oracle differs from the verified lxml path')
            if oracle[name]['summary']['namespaces'] != oracle[name]['declared_namespaces']:
                raise RuntimeError(f'{name} expanded-name URIs differ from declared URIs')
            if oracle[name]['summary'] != outputs[name]:
                raise RuntimeError(f'{name} defusedxml summary differs from the oracle: {oracle[name]["summary"]}')
        checked = run([*sandbox(ROOT / manifest['control'], scratch), '--entrypoint',
                       '/opt/venv/bin/python', base['image_id'], '-c', PARSER_CHECK]).split()
        if checked != ['defusedxml.ElementTree.DefusedXMLParser', 'xml.etree.ElementTree.XMLParser',
                       'True', 'True', 'True', 'expat_2.10.0']:
            raise RuntimeError(f'parser class, tree builder or guard check changed: {checked}')
        runs_a = [probe(overlay['image_id'], ROOT / manifest['control'], scratch, f'control-{index}')
                  for index in range(REPEATS)]
        runs_b = [probe(overlay['image_id'], ROOT / manifest['differential_control'], scratch, f'variant-{index}')
                  for index in range(REPEATS)]
    first, other = runs_a[0], runs_b[0]
    if any(item != first for item in runs_a[1:]) or any(item != other for item in runs_b[1:]):
        raise RuntimeError('repeated defusedxml/Expat source feedback is unstable')
    (py_a, et_a, expat_a), (py_b, et_b, expat_b) = split(first[0]), split(other[0])
    feature_diff = len(first[0] ^ other[0])
    tuple_diff = len(first[1] ^ other[1])
    if feature_diff == 0 or tuple_diff == 0 or not expat_a ^ expat_b:
        raise RuntimeError('Expat feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'xml/python/defusedxml', 'pass': True,
              'input_kind': 'two fixed valid UTF-8 XML 1.0 namespace controls without DOCTYPE',
              'tested_parser': checked[0], 'tested_parser_base': checked[1] + ' (pure-Python class)',
              'tree_builder': '_elementtree.TreeBuilder (C accelerator, not covered)',
              'guards_installed': ['EntityDeclHandler', 'UnparsedEntityDeclHandler', 'ExternalEntityRefHandler'],
              'expat_version': checked[5],
              'oracle': 'lxml 6.1.3 / libxml2 2.15.4 namespace-aware parse in the verified lxml image; '
                        'summary without the xmlns declaration count, namespaces from expanded names',
              'oracle_image_id': lxml_image,
              'oracle_matches_lxml_path_without_declaration_count': True,
              'oracle_name_uris_equal_declared_uris': True,
              'defusedxml_matches_oracle': True,
              'feedback_scope': 'executed Python lines of defusedxml 0.7.1 and CPython 3.14 xml/etree during the defusedxml.ElementTree.parse call, plus Expat 2.10.0 LLVM regions and branches under /work/expat/lib; harness and post-parse summary lines are excluded',
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
              'elementtree_driver_feature_difference': len(et_a ^ et_b),
              'expat_feature_difference': len(expat_a ^ expat_b),
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
