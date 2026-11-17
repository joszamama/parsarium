"""Check jxmlease against raw-name oracles and its Python/Expat feedback on two fixed, valid XML controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/xml/python/jxmlease'
OVERLAY = ROOT / 'fuzzing/afl-native/xml/python/jxmlease'
LXML = ROOT / 'projects/xml/python/lxml'
REPORT = ROOT / 'data/python/xml/jxmlease-valid-feedback.json'
PACKAGES = '/opt/venv/lib/python3.14/site-packages/'
JXMLEASE = PACKAGES + 'jxmlease/'
EXPAT = '/work/expat/lib/'
REQUIRED = (JXMLEASE + '_parsehandler.py:', JXMLEASE + 'xmlparser.py:', EXPAT + 'xmlparse.c:')
REPEATS = 5
sys.path.insert(0, str(ROOT / 'projects/xml/c/libnxml'))
from oracle import summarize as expat_raw_names  # noqa: E402  (expat, namespace processing off)

# Independent libxml2 oracle, run in the verified lxml image: the namespace-aware
# lxml tree projected back to names as written (prefix:local), with each element's
# own namespace declarations rendered as xmlns / xmlns:prefix attributes. lxml does
# not keep the source order between declarations and attributes, so attributes are
# compared as a sorted multiset; everything else is compared exactly.
ORACLE = r'''
import json, sys
from lxml import etree

parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=False)
root = etree.parse(sys.argv[1], parser).getroot()
state = {"attributes": [], "elements": [], "max_depth": 0, "text": []}

def raw(element_or_none, qname, nsmap):
    name = etree.QName(qname)
    if not name.namespace:
        return name.localname
    prefixes = [p for p, uri in nsmap.items() if uri == name.namespace]
    prefix = prefixes[0] if prefixes else None
    return (prefix + ":" if prefix else "") + name.localname

def walk(element, depth, inherited):
    state["elements"].append(raw(element, element.tag, {element.prefix: etree.QName(element).namespace} if etree.QName(element).namespace else {}))
    state["max_depth"] = max(state["max_depth"], depth)
    for prefix in element.nsmap.keys() | inherited.keys():
        if element.nsmap.get(prefix) != inherited.get(prefix):
            state["attributes"].append(("xmlns:" + prefix if prefix else "xmlns") + "=" + (element.nsmap.get(prefix) or ""))
    for key, value in element.attrib.items():
        named = {p: u for p, u in element.nsmap.items() if p}
        state["attributes"].append(raw(element, key, named) + "=" + value)
    joined = (element.text or "") + "".join(child.tail or "" for child in element)
    if joined.strip():
        state["text"].append(joined.strip())
    for child in element:
        if isinstance(child.tag, str):
            walk(child, depth + 1, element.nsmap)

walk(root, 1, {})
state["root"] = state["elements"][0]
state["attributes"].sort()
print(json.dumps(state, ensure_ascii=False))
'''


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
    if not features or not tuples or any(not value.startswith((JXMLEASE, EXPAT)) for value in features):
        raise RuntimeError('feedback is empty or outside jxmlease/Expat source')
    for required in REQUIRED:
        if not any(value.startswith(required) for value in features):
            raise RuntimeError(f'{required} has no feedback')
    return features, tuples


def split(features: set[str]) -> tuple[set[str], set[str]]:
    return ({value for value in features if value.startswith(JXMLEASE)},
            {value for value in features if value.startswith(EXPAT)})


def main() -> None:
    manifest = json.loads((PROJECT / 'manifest.json').read_text())
    base = json.loads((PROJECT / 'verification.json').read_text())
    overlay = json.loads((OVERLAY / 'verification.json').read_text())
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
    with tempfile.TemporaryDirectory(prefix='parsarium-jxmlease-feedback-') as temporary:
        scratch = Path(temporary)
        outputs, lxml_oracle = {}, {}
        for name, path, _, key in controls:
            source = ROOT / path
            outputs[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                            '/opt/venv/bin/python', base['image_id'],
                                            '/work/replay.py', '/input/case']))
            if outputs[name] != manifest[key]:
                raise RuntimeError(f'{name} jxmlease summary changed: {outputs[name]}')
            if expat_raw_names(source.read_bytes()) != outputs[name]:
                raise RuntimeError(f'{name} differs from the expat raw-name oracle')
            lxml_oracle[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                                '/opt/venv/bin/python', lxml_image,
                                                '-c', ORACLE, '/input/case']))
            projected = {**outputs[name], 'attributes': sorted(outputs[name]['attributes'])}
            if lxml_oracle[name] != projected:
                raise RuntimeError(f'{name} differs from the lxml raw-name projection: {lxml_oracle[name]}')
        checked = run([*sandbox(ROOT / manifest['control'], scratch), '--entrypoint',
                       '/opt/venv/bin/python', base['image_id'], '-c',
                       'import pyexpat, jxmlease.xmlparser as xp; p = xp.Parser(); '
                       'print(xp.expat.ParserCreate is pyexpat.ParserCreate, p._process_namespaces, '
                       'pyexpat.EXPAT_VERSION)']).split()
        if checked != ['True', 'False', 'expat_2.10.0']:
            raise RuntimeError(f'jxmlease parser or namespace mode changed: {checked}')
        runs_a = [probe(overlay['image_id'], ROOT / manifest['control'], scratch, f'control-{index}')
                  for index in range(REPEATS)]
        runs_b = [probe(overlay['image_id'], ROOT / manifest['differential_control'], scratch, f'variant-{index}')
                  for index in range(REPEATS)]
    first, other = runs_a[0], runs_b[0]
    if any(item != first for item in runs_a[1:]) or any(item != other for item in runs_b[1:]):
        raise RuntimeError('repeated jxmlease/Expat source feedback is unstable')
    (py_a, expat_a), (py_b, expat_b) = split(first[0]), split(other[0])
    feature_diff = len(first[0] ^ other[0])
    tuple_diff = len(first[1] ^ other[1])
    if feature_diff == 0 or tuple_diff == 0 or not expat_a ^ expat_b:
        raise RuntimeError('Expat feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'xml/python/jxmlease', 'pass': True,
              'input_kind': 'two fixed valid UTF-8 XML 1.0 namespace controls without DOCTYPE',
              'parser_create_is_pyexpat': True, 'process_namespaces': False, 'expat_version': checked[2],
              'view': 'raw names as written (prefix:local); xmlns declarations are ordinary attributes; no namespace URI resolved',
              'oracles': ['projects/xml/c/libnxml/oracle.py (CPython pyexpat, namespace processing off; exact match)',
                          'lxml 6.1.3 / libxml2 2.15.4 parse in the verified lxml image projected to raw names (attributes compared as a sorted multiset)'],
              'oracle_image_id': lxml_image,
              'expat_oracle_matches': True, 'lxml_projection_matches': True,
              'feedback_scope': 'executed Python lines of jxmlease 1.0.3 during the jxmlease.parse call, plus Expat 2.10.0 LLVM regions and branches under /work/expat/lib; harness and post-parse summary lines are excluded',
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'],
              'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'repeated_control_runs': REPEATS, 'control_repeat_identical': True,
              'repeated_variant_runs': REPEATS, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'control_jxmlease_features': len(py_a), 'variant_jxmlease_features': len(py_b),
              'control_expat_features': len(expat_a), 'variant_expat_features': len(expat_b),
              'parser_feature_difference': feature_diff,
              'jxmlease_feature_difference': len(py_a ^ py_b),
              'expat_feature_difference': len(expat_a ^ expat_b),
              'changed_jxmlease_lines': sorted(py_a ^ py_b),
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v for k, v in report.items() if 'output' not in k}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
