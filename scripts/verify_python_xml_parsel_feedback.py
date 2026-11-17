"""Check Parsel + libxml2 source feedback and the expat oracle on two fixed, valid XML controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/xml/python/parsel'
OVERLAY = ROOT / 'fuzzing/afl-native/xml/python/parsel'
REPORT = ROOT / 'data/python/xml/parsel-valid-feedback.json'
PARSEL = '/opt/venv/lib/python3.14/site-packages/parsel/'
LIBXML2 = '/work/libxml2/parser.c:'
REQUIRED = (PARSEL + 'selector.py:', LIBXML2)
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
    if not features or not tuples or any(not value.startswith((PARSEL, LIBXML2)) for value in features):
        raise RuntimeError('feedback is empty or outside parsel/libxml2 parser.c source')
    for required in REQUIRED:
        if not any(value.startswith(required) for value in features):
            raise RuntimeError(f'{required} has no feedback')
    return features, tuples


def split(features: set[str]) -> tuple[set[str], set[str]]:
    return ({value for value in features if value.startswith(PARSEL)},
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
    with tempfile.TemporaryDirectory(prefix='parsarium-parsel-feedback-') as temporary:
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
        if oracle != outputs:
            raise RuntimeError(f'expat oracle disagrees: {oracle}')
        facts = run([*sandbox(control, scratch), '--entrypoint', '/opt/venv/bin/python',
                     base['image_id'], '-c',
                     'import pyexpat; from parsel import Selector; from parsel.selector import _ctgroup; '
                     's = Selector(body=b"<r/>", type="xml"); p = _ctgroup["xml"]["_parser"]; '
                     'print(p.__module__ + "." + p.__name__, p.__mro__[1].__module__ + "." + p.__mro__[1].__name__, '
                     'type(s.root).__module__ + "." + type(s.root).__name__, pyexpat.EXPAT_VERSION)']).split()
        if facts[:3] != ['parsel.selector.SafeXMLParser', 'lxml.etree.XMLParser', 'lxml.etree._Element']:
            raise RuntimeError(f'"xml" Selector parser is {facts}')
        controls = [probe(overlay['image_id'], control, scratch, f'control-{index}') for index in range(REPEATS)]
        variants = [probe(overlay['image_id'], variant, scratch, f'variant-{index}') for index in range(REPEATS)]
    first, other = controls[0], variants[0]
    if any(item != first for item in controls[1:]) or any(item != other for item in variants[1:]):
        raise RuntimeError('repeated parsel/libxml2 source feedback is unstable')
    feature_diff = len(first[0] ^ other[0])
    tuple_diff = len(first[1] ^ other[1])
    (parsel_a, xml_a), (parsel_b, xml_b) = split(first[0]), split(other[0])
    # Parsel's own lines may not depend on valid input; libxml2's must.
    if feature_diff == 0 or tuple_diff == 0 or not xml_a ^ xml_b:
        raise RuntimeError('libxml2 feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'xml/python/parsel', 'pass': True,
              'input_kind': 'two fixed valid UTF-8 XML 1.0 namespace controls without DOCTYPE',
              'tested_parser': facts[0], 'tested_parser_base': facts[1], 'tested_root_type': facts[2],
              'oracle': 'projects/xml/python/parsel/oracle.py (CPython pyexpat, namespace mode)',
              'oracle_expat_version': facts[3],
              'oracle_matches_control': True, 'oracle_matches_variant': True,
              'feedback_scope': 'executed Python lines of the installed parsel 1.12.1 package plus libxml2 2.15.4 parser.c source lines (LLVM regions) reached through lxml 6.1.3; harness, Parsel dependencies, lxml Cython binding, libxml2 xpath.c and other libxml2 files are excluded',
              'excluded_parser_c_line_range': [8700, 8720],
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'],
              'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'repeated_control_runs': REPEATS, 'control_repeat_identical': True,
              'repeated_variant_runs': REPEATS, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'control_parsel_features': len(parsel_a), 'variant_parsel_features': len(parsel_b),
              'control_libxml2_features': len(xml_a), 'variant_libxml2_features': len(xml_b),
              'parser_feature_difference': feature_diff,
              'parsel_feature_difference': len(parsel_a ^ parsel_b),
              'libxml2_feature_difference': len(xml_a ^ xml_b),
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
