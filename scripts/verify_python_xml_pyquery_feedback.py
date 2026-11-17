"""Check pyquery + libxml2 source feedback and the expat oracle on two fixed, valid XML controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/xml/python/pyquery'
OVERLAY = ROOT / 'fuzzing/afl-native/xml/python/pyquery'
REPORT = ROOT / 'data/python/xml/pyquery-valid-feedback.json'
PYQUERY = '/opt/venv/lib/python3.14/site-packages/pyquery/'
LIBXML2 = '/work/libxml2/parser.c:'
REQUIRED = (PYQUERY + 'pyquery.py:', LIBXML2)
REPEATS = 5


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
    if not features or not tuples or any(not value.startswith((PYQUERY, LIBXML2)) for value in features):
        raise RuntimeError('feedback is empty or outside pyquery/libxml2 parser.c source')
    for required in REQUIRED:
        if not any(value.startswith(required) for value in features):
            raise RuntimeError(f'{required} has no feedback')
    return features, tuples


def split(features: set[str]) -> tuple[set[str], set[str]]:
    return ({value for value in features if value.startswith(PYQUERY)},
            {value for value in features if value.startswith(LIBXML2)})


def main() -> None:
    manifest = json.loads((PROJECT / 'manifest.json').read_text())
    base = json.loads((PROJECT / 'verification.json').read_text())
    overlay = json.loads((OVERLAY / 'verification.json').read_text())
    if overlay['base_image_id'] != base['image_id']:
        raise RuntimeError('AFL overlay base differs from verified project')
    if overlay['base_project_receipt_sha256'] != sha256((PROJECT / 'verification.json').read_bytes()).hexdigest():
        raise RuntimeError('AFL overlay was built from a different project receipt')
    control = ROOT / manifest['control']
    variant = ROOT / manifest['differential_control']
    for source, digest in ((control, manifest['control_sha256']),
                           (variant, manifest['differential_control_sha256'])):
        if sha256(source.read_bytes()).hexdigest() != digest:
            raise RuntimeError('valid control hash changed')
    with tempfile.TemporaryDirectory(prefix='parsarium-pyquery-feedback-') as temporary:
        scratch = Path(temporary)
        outputs, oracle = {}, {}
        for name, source in (('control', control), ('variant', variant)):
            outputs[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                            '/opt/venv/bin/python', base['image_id'],
                                            '/work/replay.py', '/input/case']))
            # The oracle runs on the image's system Python: pyexpat, no lxml or libxml2.
            oracle[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                           '/usr/bin/python3', base['image_id'],
                                           '-I', '/work/oracle.py', '/input/case']))
        if outputs['control'] != manifest['expected_output']:
            raise RuntimeError(f'catalog control summary changed: {outputs["control"]}')
        if outputs['variant'] != manifest['differential_expected_output']:
            raise RuntimeError(f'order control summary changed: {outputs["variant"]}')
        # pyquery reports no comments or processing instructions; compare the keys it reports.
        oracle = {name: {key: value for key, value in oracle[name].items() if key in outputs[name]}
                  for name in oracle}
        if oracle != outputs:
            raise RuntimeError(f'expat oracle disagrees: {oracle}')
        facts = run([*sandbox(control, scratch), '--entrypoint', '/opt/venv/bin/python',
                     base['image_id'], '-c',
                     'import pyexpat, inspect; from lxml import etree; from pyquery import PyQuery; '
                     'from pyquery.pyquery import fromstring; d = PyQuery(b"<r/>", parser="xml"); '
                     'assert "custom_parser = getattr(etree, meth)" in inspect.getsource(fromstring); '
                     'print("lxml.etree.fromstring", type(d[0]).__module__ + "." + type(d[0]).__name__, '
                     '".".join(map(str, etree.LIBXML_VERSION)), pyexpat.EXPAT_VERSION)']).split()
        if facts[:2] != ['lxml.etree.fromstring', 'lxml.etree._Element']:
            raise RuntimeError(f'parser="xml" path is {facts}')
        controls = [probe(overlay['image_id'], control, scratch, f'control-{index}') for index in range(REPEATS)]
        variants = [probe(overlay['image_id'], variant, scratch, f'variant-{index}') for index in range(REPEATS)]
    first, other = controls[0], variants[0]
    if any(item != first for item in controls[1:]) or any(item != other for item in variants[1:]):
        raise RuntimeError('repeated pyquery/libxml2 source feedback is unstable')
    feature_diff = len(first[0] ^ other[0])
    tuple_diff = len(first[1] ^ other[1])
    (pyquery_a, xml_a), (pyquery_b, xml_b) = split(first[0]), split(other[0])
    # pyquery's own lines may not depend on valid input; libxml2's must.
    if feature_diff == 0 or tuple_diff == 0 or not xml_a ^ xml_b:
        raise RuntimeError('libxml2 feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'xml/python/pyquery', 'pass': True,
              'input_kind': 'two fixed valid UTF-8 XML 1.0 namespace controls without DOCTYPE',
              'tested_parser': facts[0], 'tested_root_type': facts[1], 'libxml2_version': facts[2],
              'oracle': 'projects/xml/python/pyquery/oracle.py (CPython pyexpat, namespace mode; comment and PI keys not compared)',
              'oracle_expat_version': facts[3],
              'oracle_matches_control': True, 'oracle_matches_variant': True,
              'feedback_scope': 'executed Python lines of the installed pyquery 2.1.0 package plus libxml2 2.15.4 parser.c source lines (LLVM regions) reached through lxml 6.1.3; harness, cssselect, lxml Cython binding, libxml2 xpath.c and other libxml2 files are excluded',
              'excluded_parser_c_line_range': [8700, 8720],
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'],
              'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'repeated_control_runs': REPEATS, 'control_repeat_identical': True,
              'repeated_variant_runs': REPEATS, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'control_pyquery_features': len(pyquery_a), 'variant_pyquery_features': len(pyquery_b),
              'control_libxml2_features': len(xml_a), 'variant_libxml2_features': len(xml_b),
              'parser_feature_difference': feature_diff,
              'pyquery_feature_difference': len(pyquery_a ^ pyquery_b),
              'libxml2_feature_difference': len(xml_a ^ xml_b),
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
