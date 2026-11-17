"""Check untangle against an lxml oracle and its SAX/Expat feedback on two fixed, valid XML controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/xml/python/untangle'
OVERLAY = ROOT / 'fuzzing/afl-native/xml/python/untangle'
LXML = ROOT / 'projects/xml/python/lxml'
REPORT = ROOT / 'data/python/xml/untangle-valid-feedback.json'
PACKAGES = '/opt/venv/lib/python3.14/site-packages/'
UNTANGLE = PACKAGES + 'untangle/__init__.py:'
SAX = '/usr/lib/python3.14/xml/sax/'
EXPAT = '/work/expat/lib/'
REQUIRED = (UNTANGLE, PACKAGES + 'defusedxml/expatreader.py:', SAX + 'expatreader.py:', EXPAT + 'xmlparse.c:')
REPEATS = 5

# Namespace-aware libxml2 oracle, run in the verified lxml image. It reports the
# lxml path's expanded summary and the same tree projected to untangle's
# documented view: qualified names with '-', '.', ':' -> '_' (keywords get '_'),
# raw qualified attribute names, xmlns declarations and per-element text.
ORACLE = r'''
import json, keyword, sys
from lxml import etree

def mangle(name):
    name = name.replace("-", "_").replace(".", "_").replace(":", "_")
    return name + "_" if keyword.iskeyword(name) else name

parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=False)
root = etree.parse(sys.argv[1], parser).getroot()
keys = ("attributes", "elements", "max_depth", "namespace_declarations", "namespaces", "text")
expanded = {key: [] for key in keys}
projected = {key: [] for key in keys}
for state in (expanded, projected):
    state.update(max_depth=0, namespace_declarations=0, namespaces=set())
pairs = {"elements": [], "attributes": []}

def text(value):
    if value and value.strip():
        expanded["text"].append(value.strip())

def walk(element, depth, inherited):
    name = etree.QName(element)
    qualified = (element.prefix + ":" if element.prefix else "") + name.localname
    expanded["elements"].append(element.tag)
    projected["elements"].append(mangle(qualified))
    pairs["elements"].append([element.tag, mangle(qualified)])
    for state in (expanded, projected):
        state["max_depth"] = max(state["max_depth"], depth)
    for prefix, uri in element.nsmap.items():
        if inherited.get(prefix) != uri:
            for state in (expanded, projected):
                state["namespace_declarations"] += 1
                if uri:
                    state["namespaces"].add(uri)
    for key, value in element.attrib.items():
        attribute = etree.QName(key)
        raw = attribute.localname
        if attribute.namespace:
            prefix, = [p for p, uri in element.nsmap.items() if p and uri == attribute.namespace]
            raw = prefix + ":" + raw
        expanded["attributes"].append(key + "=" + value)
        projected["attributes"].append(raw + "=" + value)
        pairs["attributes"].append([key, raw])
    joined = (element.text or "") + "".join(child.tail or "" for child in element)
    if joined.strip():
        projected["text"].append(joined.strip())
    text(element.text)
    for child in element:
        if isinstance(child.tag, str):
            walk(child, depth + 1, element.nsmap)
        text(child.tail)

walk(root, 1, {})
for state in (expanded, projected):
    state["namespaces"] = sorted(state["namespaces"])
expanded["root"] = root.tag
projected["root"] = pairs["elements"][0][1]
print(json.dumps({"expanded": expanded, "projected": projected, "pairs": pairs}, ensure_ascii=False))
'''

PARSER_CHECK = ('import pyexpat, untangle, xml.sax.expatreader; from pathlib import Path; '
                'from defusedxml.sax import make_parser; p = make_parser(); '
                'd = untangle.parse(Path("/input/case"), feature_namespaces=True); '
                'print(type(p).__module__ + "." + type(p).__name__, '
                'isinstance(p, xml.sax.expatreader.ExpatParser), pyexpat.EXPAT_VERSION, len(d.children))')


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
    if not features or not tuples or any(not value.startswith((PACKAGES, SAX, EXPAT)) for value in features):
        raise RuntimeError('feedback is empty or outside untangle/defusedxml/SAX driver/Expat source')
    for required in REQUIRED:
        if not any(value.startswith(required) for value in features):
            raise RuntimeError(f'{required} has no feedback')
    return features, tuples


def split(features: set[str]) -> tuple[set[str], set[str], set[str]]:
    return ({value for value in features if value.startswith(PACKAGES)},
            {value for value in features if value.startswith(SAX)},
            {value for value in features if value.startswith(EXPAT)})


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
    with tempfile.TemporaryDirectory(prefix='parsarium-untangle-feedback-') as temporary:
        scratch = Path(temporary)
        outputs, oracle = {}, {}
        for name, path, _, key in controls:
            source = ROOT / path
            outputs[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                            '/opt/venv/bin/python', base['image_id'],
                                            '/work/replay.py', '/input/case']))
            if outputs[name] != manifest[key]:
                raise RuntimeError(f'{name} untangle summary changed: {outputs[name]}')
            oracle[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                           '/opt/venv/bin/python', lxml_image,
                                           '-c', ORACLE, '/input/case']))
            if oracle[name]['expanded'] != lxml_manifest[key]:
                raise RuntimeError(f'{name} oracle differs from the verified lxml path')
            if oracle[name]['projected'] != outputs[name]:
                raise RuntimeError(f'{name} untangle summary differs from the projected oracle: '
                                   f'{oracle[name]["projected"]}')
        checked = run([*sandbox(ROOT / manifest['control'], scratch), '--entrypoint',
                       '/opt/venv/bin/python', base['image_id'], '-c', PARSER_CHECK]).split()
        if checked != ['defusedxml.expatreader.DefusedExpatParser', 'True', 'expat_2.10.0', '0']:
            raise RuntimeError(f'SAX parser or namespace-mode check changed: {checked}')
        runs_a = [probe(overlay['image_id'], ROOT / manifest['control'], scratch, f'control-{index}')
                  for index in range(REPEATS)]
        runs_b = [probe(overlay['image_id'], ROOT / manifest['differential_control'], scratch, f'variant-{index}')
                  for index in range(REPEATS)]
    first, other = runs_a[0], runs_b[0]
    if any(item != first for item in runs_a[1:]) or any(item != other for item in runs_b[1:]):
        raise RuntimeError('repeated untangle/Expat source feedback is unstable')
    (py_a, sax_a, expat_a), (py_b, sax_b, expat_b) = split(first[0]), split(other[0])
    feature_diff = len(first[0] ^ other[0])
    tuple_diff = len(first[1] ^ other[1])
    if feature_diff == 0 or tuple_diff == 0 or not expat_a ^ expat_b:
        raise RuntimeError('Expat feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    dropped = {name: {kind: [pair for pair in oracle[name]['pairs'][kind] if pair[0] != pair[1]]
                      for kind in ('elements', 'attributes')} for name in oracle}
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'xml/python/untangle', 'pass': True,
              'input_kind': 'two fixed valid UTF-8 XML 1.0 namespace controls without DOCTYPE',
              'tested_sax_parser': checked[0], 'expat_version': checked[2],
              'feature_namespaces_true_root_children': int(checked[3]),
              'oracle': 'lxml 6.1.3 / libxml2 2.15.4 namespace-aware parse in the verified lxml image, '
                        'projected to untangle qualified-name output with the documented "-", ".", ":" -> "_" rule',
              'oracle_image_id': lxml_image,
              'oracle_expanded_matches_lxml_path': True, 'untangle_matches_projected_oracle': True,
              'namespace_uris_dropped': dropped,
              'feedback_scope': 'executed Python lines of untangle 1.3.1, defusedxml 0.7.1 and CPython 3.14 xml/sax during the untangle.parse call, plus Expat 2.10.0 LLVM regions and branches under /work/expat/lib; harness and post-parse summary lines are excluded',
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'],
              'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'repeated_control_runs': REPEATS, 'control_repeat_identical': True,
              'repeated_variant_runs': REPEATS, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'control_package_features': len(py_a), 'variant_package_features': len(py_b),
              'control_sax_driver_features': len(sax_a), 'variant_sax_driver_features': len(sax_b),
              'control_expat_features': len(expat_a), 'variant_expat_features': len(expat_b),
              'parser_feature_difference': feature_diff,
              'package_feature_difference': len(py_a ^ py_b),
              'sax_driver_feature_difference': len(sax_a ^ sax_b),
              'expat_feature_difference': len(expat_a ^ expat_b),
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
