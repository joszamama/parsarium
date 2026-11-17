"""Check Beautiful Soup + libxml2 source feedback on two fixed, valid XML controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/xml/python/beautifulsoup4'
OVERLAY = ROOT / 'fuzzing/afl-native/xml/python/beautifulsoup4'
REPORT = ROOT / 'data/python/xml/beautifulsoup4-valid-feedback.json'
BS4 = '/opt/venv/lib/python3.14/site-packages/bs4/'
LIBXML2 = '/work/libxml2/parser.c:'
REQUIRED = (BS4 + 'builder/_lxml.py:', BS4 + 'element.py:', BS4 + '__init__.py:', LIBXML2)
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
    if not features or not tuples or any(not value.startswith((BS4, LIBXML2)) for value in features):
        raise RuntimeError('feedback is empty or outside bs4/libxml2 parser.c source')
    for required in REQUIRED:
        if not any(value.startswith(required) for value in features):
            raise RuntimeError(f'{required} has no feedback')
    return features, tuples


def split(features: set[str]) -> tuple[set[str], set[str]]:
    return ({value for value in features if value.startswith(BS4)},
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
    with tempfile.TemporaryDirectory(prefix='parsarium-bs4-feedback-') as temporary:
        scratch = Path(temporary)
        outputs = {}
        for name, source in (('control', control), ('variant', variant)):
            outputs[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                            '/opt/venv/bin/python', base['image_id'],
                                            '/work/replay.py', '/input/case']))
        if outputs['control'] != manifest['expected_output']:
            raise RuntimeError(f'catalog control tree changed: {outputs["control"]}')
        if outputs['variant'] != manifest['differential_expected_output']:
            raise RuntimeError(f'order control tree changed: {outputs["variant"]}')
        builder = run([*sandbox(control, scratch), '--entrypoint', '/opt/venv/bin/python',
                       base['image_id'], '-c',
                       'from bs4 import BeautifulSoup; b = BeautifulSoup(b"<r/>", "xml").builder; '
                       'print(type(b).__module__ + "." + type(b).__name__, type(b.parser_for("utf-8")).__module__ '
                       '+ "." + type(b.parser_for("utf-8")).__name__)']).split()
        if builder != ['bs4.builder._lxml.LXMLTreeBuilderForXML', 'lxml.etree.XMLParser']:
            raise RuntimeError(f'"xml" builder is {builder}')
        controls = [probe(overlay['image_id'], control, scratch, f'control-{index}') for index in range(REPEATS)]
        variants = [probe(overlay['image_id'], variant, scratch, f'variant-{index}') for index in range(REPEATS)]
    first, other = controls[0], variants[0]
    if any(item != first for item in controls[1:]) or variants[1] != other:
        raise RuntimeError('repeated bs4/libxml2 source feedback is unstable')
    feature_diff = len(first[0] ^ other[0])
    tuple_diff = len(first[1] ^ other[1])
    (bs4_a, xml_a), (bs4_b, xml_b) = split(first[0]), split(other[0])
    if feature_diff == 0 or tuple_diff == 0 or not bs4_a ^ bs4_b or not xml_a ^ xml_b:
        raise RuntimeError('bs4 or libxml2 feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'xml/python/beautifulsoup4', 'pass': True,
              'input_kind': 'two fixed valid UTF-8 XML 1.0 namespace controls without DOCTYPE',
              'tested_builder': builder[0], 'tested_lxml_parser_class': builder[1],
              'feedback_scope': 'executed Python lines of the installed bs4 4.15.0 package plus libxml2 2.15.4 parser.c source lines (LLVM regions) reached through lxml 6.1.3; harness, lxml Cython binding and other libxml2 files are excluded',
              'excluded_parser_c_line_range': [8700, 8720],
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'],
              'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'repeated_control_runs': REPEATS, 'control_repeat_identical': True,
              'repeated_variant_runs': REPEATS, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'control_bs4_features': len(bs4_a), 'variant_bs4_features': len(bs4_b),
              'control_libxml2_features': len(xml_a), 'variant_libxml2_features': len(xml_b),
              'parser_feature_difference': feature_diff,
              'bs4_feature_difference': len(bs4_a ^ bs4_b),
              'libxml2_feature_difference': len(xml_a ^ xml_b),
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
