"""Verify stable libxml2-source AFL++ feedback on two fixed valid XML controls."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
IMAGE = 'parsarium-afl/xml-python-lxml:local'
SAMPLES = {'control': ROOT / 'controls/xml/catalog-ns.xml',
           'variant': ROOT / 'controls/xml/order-default-ns.xml'}


def run(args):
    result = subprocess.run(args, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1500:])


def probe(source, scratch, label):
    common = ['docker', 'run', '--rm', '--platform', 'linux/arm64', '--network', 'none',
              '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
              '--user', f'{os.getuid()}:{os.getgid()}', '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
              '-v', f'{source}:/input/case:ro', '-v', f'{scratch}:/coverage']
    features = scratch / f'{label}.features'
    edges = scratch / f'{label}.edges'
    run([*common, '--entrypoint', '/bin/sh', IMAGE,
         '/work/afl_trace', '/input/case', f'/coverage/{features.name}'])
    run([*common, '-e', 'AFL_MAP_SIZE=65536', '--entrypoint', 'afl-showmap', IMAGE,
         '-m', 'none', '-t', '120000', '-o', f'/coverage/{edges.name}', '--',
         '/work/afl_proxy', '/input/case'])
    feature_set = set(features.read_text().splitlines()) - {''}
    edge_set = {line.split(':', 1)[0] for line in edges.read_text().splitlines() if line}
    if not feature_set or not edge_set or not all(item.startswith('/work/libxml2/parser.c:') for item in feature_set):
        raise RuntimeError('missing scoped libxml2 parser feedback')
    return feature_set, edge_set


def main():
    receipt_path = ROOT / 'fuzzing/afl-native/xml/python/lxml/verification.json'
    receipt = json.loads(receipt_path.read_text())
    if not receipt['pass'] or receipt['feedback_kind'] != 'llvm_native_parser_regions_to_afl_bitmap':
        raise RuntimeError('no verified native parser bridge')
    inspected = subprocess.run(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}'],
                               capture_output=True, text=True, check=True).stdout.strip()
    if inspected != receipt['image_id']:
        raise RuntimeError('AFL++ image tag differs from verification receipt')
    with tempfile.TemporaryDirectory(prefix='parsarium-lxml-feedback-') as dirname:
        scratch = Path(dirname)
        repeated = [probe(SAMPLES['control'], scratch, f'control-{index}')
                    for index in range(5)]
        first = repeated[0]
        variant = probe(SAMPLES['variant'], scratch, 'variant')
    if any(item != first for item in repeated[1:]):
        raise RuntimeError('repeated control feedback changed')
    feature_difference = len(first[0] ^ variant[0])
    edge_difference = len(first[1] ^ variant[1])
    if feature_difference == 0 or edge_difference == 0:
        raise RuntimeError('valid differential input did not change native parser feedback')
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'xml/python/lxml', 'pass': True,
              'overlay_receipt_sha256': sha256(receipt_path.read_bytes()).hexdigest(),
              'image_id': inspected,
              'feedback_scope': 'executed parser.c source lines in source-built libxml2 2.15.4',
              'control_sha256': sha256(SAMPLES['control'].read_bytes()).hexdigest(),
              'variant_sha256': sha256(SAMPLES['variant'].read_bytes()).hexdigest(),
              'repeated_control_identical': True,
              'repeated_control_runs': len(repeated),
              'excluded_parser_c_line_range': [8700, 8720],
              'control_parser_features': len(first[0]),
              'variant_parser_features': len(variant[0]),
              'parser_feature_symmetric_difference': feature_difference,
              'control_afl_edge_ids': len(first[1]),
              'variant_afl_edge_ids': len(variant[1]),
              'afl_edge_id_symmetric_difference': edge_difference}
    output = ROOT / 'data/python/xml/lxml-valid-feedback.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
