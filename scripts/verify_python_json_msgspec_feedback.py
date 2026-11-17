"""Check msgspec _core.c JSON decoder feedback on two fixed, valid JSON controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/json/python/msgspec'
OVERLAY = ROOT / 'fuzzing/afl-native/json/python/msgspec'
REPORT = ROOT / 'data/python/json/msgspec-valid-feedback.json'
PREFIX = '/work/msgspec-source/src/msgspec/'
CORE = PREFIX + '_core.c'
BANNERS = {'json_decoder_lines': ('JSON Decoder', 'to_builtins'),
           'number_parser_lines': ('Number Parser', 'MessagePack Encoder')}


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


def in_section(feature: str, lines: range) -> bool:
    filename, line, *_ = feature.rsplit(':', 3) if feature.endswith(('true', 'false')) \
        else feature.rsplit(':', 2)
    return filename == CORE and int(line) in lines


def probe(image: str, source: Path, scratch: Path, label: str) -> tuple[set[str], set[str], set[str]]:
    base = sandbox(source, scratch)
    run([*base, '--entrypoint', '/bin/sh', image,
         '/work/afl_trace', '/input/case', f'/coverage/{label}.features'])
    maps = []
    for suffix, extra in (('map', []), ('raw.map', ['-r'])):
        run([*base, '-e', 'AFL_MAP_SIZE=65536', '--entrypoint', 'afl-showmap', image,
             '-m', 'none', '-t', '120000', *extra, '-o', f'/coverage/{label}.{suffix}',
             '--', '/work/afl_proxy', '/input/case'])
        maps.append({line.split(':', 1)[0] for line in
                     (scratch / f'{label}.{suffix}').read_text().splitlines() if line})
    features = set((scratch / f'{label}.features').read_text().splitlines()) - {''}
    if not features or not maps[0] or any(not value.startswith(PREFIX) for value in features):
        raise RuntimeError('feedback is empty or outside msgspec source')
    return features, maps[0], maps[1]


def main() -> None:
    manifest = json.loads((PROJECT / 'manifest.json').read_text())
    base = json.loads((PROJECT / 'verification.json').read_text())
    overlay = json.loads((OVERLAY / 'verification.json').read_text())
    if overlay['base_image_id'] != base['image_id']:
        raise RuntimeError('AFL overlay base differs from verified project')
    if overlay['base_project_receipt_sha256'] != sha256((PROJECT / 'verification.json').read_bytes()).hexdigest():
        raise RuntimeError('AFL overlay was built from a different project receipt')
    sections = manifest['json_parser_source_sections']
    ranges = {name: range(sections[name][0], sections[name][1] + 1) for name in BANNERS}
    control = ROOT / manifest['control']
    variant = ROOT / manifest['differential_control']
    for source, digest in ((control, manifest['control_sha256']),
                           (variant, manifest['differential_control_sha256'])):
        if sha256(source.read_bytes()).hexdigest() != digest:
            raise RuntimeError('valid control hash changed')
    with tempfile.TemporaryDirectory(prefix='parsarium-msgspec-feedback-') as temporary:
        scratch = Path(temporary)
        # The section ranges must still start at their banners and end before the next one.
        for name, (start_title, next_title) in BANNERS.items():
            first, last = sections[name]
            text = run([*sandbox(control, scratch), '--entrypoint', 'sed', base['image_id'],
                        '-n', f'{first + 1}p;{last + 2}p', CORE]).splitlines()
            if start_title not in text[0] or next_title not in text[1]:
                raise RuntimeError(f'{name} no longer matches _core.c section banners: {text}')
        outputs = {}
        for name, source in (('control', control), ('variant', variant)):
            outputs[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                            '/opt/venv/bin/python', base['image_id'],
                                            '/work/replay.py', '/input/case']))
        if outputs['control'] != manifest['expected_output']:
            raise RuntimeError(f'nested object tree changed: {outputs["control"]}')
        if outputs['variant'] != manifest['differential_expected_output']:
            raise RuntimeError(f'nested array tree changed: {outputs["variant"]}')
        first = probe(overlay['image_id'], control, scratch, 'first')
        repeat = probe(overlay['image_id'], control, scratch, 'repeat')
        other = probe(overlay['image_id'], variant, scratch, 'other')
        other_repeat = probe(overlay['image_id'], variant, scratch, 'other-repeat')
    if first != repeat or other != other_repeat:
        raise RuntimeError('repeated msgspec source feedback is unstable')
    feature_diff = len(first[0] ^ other[0])
    tuple_diff = len(first[1] ^ other[1])
    raw_tuple_diff = len(first[2] ^ other[2])
    if feature_diff == 0 or tuple_diff == 0:
        raise RuntimeError('msgspec/AFL feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    decoder = {name: [{value for value in features if in_section(value, lines)}
                      for features in (first[0], other[0])]
               for name, lines in ranges.items()}
    if not all(decoder['json_decoder_lines']) or decoder['json_decoder_lines'][0] == decoder['json_decoder_lines'][1]:
        raise RuntimeError('JSON Decoder section feedback is empty or input-independent')
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'json/python/msgspec', 'pass': True,
              'input_kind': 'two fixed valid RFC 8259 JSON controls',
              'tested_api': manifest['api'],
              'feedback_scope': 'msgspec 0.22.0 own C extension source (src/msgspec/_core.c and headers) as LLVM regions and branches',
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'],
              'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'control_repeat_identical': True, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'parser_feature_difference': feature_diff,
              'json_decoder_section_lines': sections['json_decoder_lines'],
              'control_json_decoder_features': len(decoder['json_decoder_lines'][0]),
              'variant_json_decoder_features': len(decoder['json_decoder_lines'][1]),
              'json_decoder_feature_difference': len(decoder['json_decoder_lines'][0]
                                                     ^ decoder['json_decoder_lines'][1]),
              'number_parser_section_lines': sections['number_parser_lines'],
              'control_number_parser_features': len(decoder['number_parser_lines'][0]),
              'variant_number_parser_features': len(decoder['number_parser_lines'][1]),
              'number_parser_feature_difference': len(decoder['number_parser_lines'][0]
                                                      ^ decoder['number_parser_lines'][1]),
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff,
              'control_afl_raw_tuples': len(first[2]), 'variant_afl_raw_tuples': len(other[2]),
              'afl_raw_tuple_difference': raw_tuple_diff,
              'afl_tuple_note': 'afl-showmap 4.04c default output (bucketed, as in the overlay receipt) and -r raw output are both recorded.'}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
