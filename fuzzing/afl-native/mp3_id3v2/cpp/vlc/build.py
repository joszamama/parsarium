"""Build and verify AFL++ feedback from VLC's MP3 and ID3v2 parsers behind a C++17 call site.

The overlay rebuilds the pinned VLC 3.0.24 source and VLC's contrib TagLib 1.13.1
(with VLC's two contrib patches) with the same static libvlccore/libVLC
configuration as the base project. AFL++'s allowlist limits pcguard
instrumentation to the parsers on the local MP3 preparse path: TagLib and VLC's
meta_engine, skiptags, MPEG audio demuxer, and packetizer source directories.
build.sh fails if libvlccore, libVLC, file access, or the C++17
harness objects carry guards. Every tuple that afl-showmap reports therefore
comes from those parsers. A second valid tagged MP3 (the same audio frames under
an ID3v2.4 tag with UTF-8 text, where the control is ID3v2.3 with ISO-8859-1 text)
must add stable tuples absent from every control probe, and the control must keep
stable tuples absent from every variant probe. That shows the feedback follows
the parsed ID3v2 version and text encoding.

Each input is probed --repeats times (default 3) to measure stability. No
campaign is started.
"""

import argparse
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
sys.path.insert(0, str(ROOT / 'scripts'))
from docker_slots import docker_build_slot
IMAGE = f'parsarium-afl/{RELATIVE.parts[0]}-{RELATIVE.parts[1]}-{RELATIVE.parts[2]}:local'
AFL_RELEASE = '4.33c-1.1ubuntu1'
SANDBOX = ['--network', 'none', '--read-only', '--cap-drop', 'ALL',
           '--security-opt', 'no-new-privileges', '--user', f'{os.getuid()}:{os.getgid()}',
           '--tmpfs', '/tmp:rw,exec,nosuid,size=64m', '--workdir', '/tmp']
CONTROL_OUTPUT = {**MANIFEST['expected_output'], **MANIFEST['control_stream']}
VARIANT_OUTPUT = MANIFEST['valid_variant_expected_output']


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'{command[:5]} failed: {(result.stdout + result.stderr)[-3000:]}')
    return result.stdout.strip()


def replay(sample: Path) -> dict:
    return json.loads(run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                           *SANDBOX, '-v', f'{sample}:/input/sample:ro',
                           '--entrypoint', '/work/replay', IMAGE, '/input/sample']))


def showmap(map_size: int, sample: Path) -> set[str]:
    with tempfile.TemporaryDirectory(prefix='parsarium-vlc-cpp-mp3-afl-') as temporary:
        result = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
             *SANDBOX, '-e', f'AFL_MAP_SIZE={map_size}',
             '-v', f'{sample}:/input/sample:ro', '-v', f'{temporary}:/coverage',
             '--entrypoint', 'afl-showmap', IMAGE,
             '-m', 'none', '-t', '30000', '-o', '/coverage/edges.txt', '--',
             '/work/fuzzer', '/input/sample'],
             cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(f'afl-showmap failed: {(result.stdout + result.stderr)[-3000:]}')
        if not re.search(r'Captured \d+ tuples', result.stdout + result.stderr):
            raise RuntimeError('afl-showmap did not report captured tuples')
        return {line.partition(':')[0] for line in
                (Path(temporary) / 'edges.txt').read_text().splitlines() if line}


def stability(maps: list[set[str]]) -> dict:
    stable, union = set.intersection(*maps), set.union(*maps)
    return {'repeat_edge_counts': [len(edges) for edges in maps],
            'stable_edges': len(stable), 'union_edges': len(union),
            'stable_ratio': round(len(stable) / len(union), 6) if union else None,
            'all_repeats_identical': all(edges == maps[0] for edges in maps)}


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--repeats', type=int, default=3,
                     help='afl-showmap probes per input for stability (minimum 2)')
    args = cli.parse_args()
    if args.repeats < 2:
        raise SystemExit('--repeats must be at least 2')
    base_receipt = PROJECT / 'verification.json'
    if not base_receipt.is_file() or not json.loads(base_receipt.read_text()).get('pass'):
        raise RuntimeError('base VLC C++ MP3 project must be verified first')
    control = ROOT / MANIFEST['control']
    variant = PROJECT / MANIFEST['valid_variant']
    variant_hash = sha256(variant.read_bytes()).hexdigest()
    if variant_hash != MANIFEST['valid_variant_sha256'] or variant_hash != sha256(
            (ROOT / MANIFEST['valid_variant_source']).read_bytes()).hexdigest():
        raise RuntimeError('valid ID3v2.4 MP3 differs from its manifest hash or source control')
    with docker_build_slot():
        run(['docker', 'build', '--quiet', '--platform', MANIFEST['platform'],
             '-f', str(OVERLAY / 'Dockerfile'), '-t', IMAGE, str(PROJECT)])
    image_id = run(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}'])
    version = run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                   '--entrypoint', 'dpkg-query', IMAGE, '-W', '-f=${Version}', 'afl++'])
    if version != AFL_RELEASE:
        raise RuntimeError(f'AFL++ version mismatch: {version}')
    observed = replay(control)
    if observed != CONTROL_OUTPUT:
        raise RuntimeError(f'AFL-instrumented build changed control result: {observed}')
    variant_output = replay(variant)
    if variant_output != VARIANT_OUTPUT:
        raise RuntimeError(f'valid ID3v2.4 MP3 parsed unexpectedly: {variant_output}')
    probe = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                            '-e', 'AFL_DUMP_MAP_SIZE=1', '--entrypoint', '/work/fuzzer', IMAGE],
                           cwd=ROOT, capture_output=True, text=True)
    if not probe.stdout.strip().isdigit():
        raise RuntimeError(f'AFL++ map size probe failed: {probe.stderr[-2000:]}')
    map_size = int(probe.stdout.strip())
    control_maps = [showmap(map_size, control) for _ in range(args.repeats)]
    variant_maps = [showmap(map_size, variant) for _ in range(args.repeats)]
    control_edges, variant_edges = control_maps[0], variant_maps[0]
    control_union, variant_union = set.union(*control_maps), set.union(*variant_maps)
    control_stable, variant_stable = set.intersection(*control_maps), set.intersection(*variant_maps)
    if len(control_edges) < 2:
        raise RuntimeError(f'insufficient VLC MP3/ID3v2 AFL++ feedback: {len(control_edges)} edges')
    if control_edges == variant_edges:
        raise RuntimeError('ID3v2.3 control and ID3v2.4 MP3 produced identical parser feedback')
    if not variant_stable - control_union:
        raise RuntimeError('valid ID3v2.4 MP3 produced no stable new parser feedback')
    if not control_stable - variant_union:
        raise RuntimeError('ID3v2.3 control kept no stable parser feedback absent from the ID3v2.4 MP3')
    control_stability, variant_stability = stability(control_maps), stability(variant_maps)
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'vlc_mp3_id3v2_parser_pcguard_edges',
        'feedback_scope': 'TagLib 1.13.1 (VLC contrib pin and patches) and VLC 3.0.24 meta_engine, stream_filter, demux/mpeg and packetizer module sources via AFL++ allowlist; libvlccore, libVLC, file access and the C++17 harness uninstrumented',
        'shared_parser_family': MANIFEST['shared_parser_family'],
        'shared_parser_family_projects': MANIFEST['shared_parser_family_projects'],
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'source_sha256': MANIFEST['source_sha256'],
        'underlying_source_sha256': MANIFEST['underlying_source_sha256'],
        'control_sha256': MANIFEST['control_sha256'],
        'variant_sha256': variant_hash,
        'variant_output': variant_output,
        'image_id': image_id, 'platform': MANIFEST['platform'],
        'afl_package': version, 'afl_version_output': version,
        'afl_map_size': map_size,
        'repeats': args.repeats,
        'feedback_edges': len(control_edges),
        'variant_feedback_edges': len(variant_edges),
        'edges_only_in_control': len(control_edges - variant_edges),
        'edges_only_in_variant': len(variant_edges - control_edges),
        'control_stability': control_stability,
        'variant_stability': variant_stability,
        'stable_variant_only_edges': len(variant_stable - control_union),
        'stable_control_only_edges': len(control_stable - variant_union),
        'overlay_file_sha256': {
            name: sha256((OVERLAY / name).read_bytes()).hexdigest()
            for name in ('Dockerfile', 'build.py')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {len(control_edges)} VLC MP3/ID3v2 AFL++ feedback edges, '
          f'{receipt["stable_variant_only_edges"]} stable edges only in the ID3v2.4 MP3, '
          f'{receipt["stable_control_only_edges"]} only in the ID3v2.3 control, '
          f'control stable ratio {control_stability["stable_ratio"]} over {args.repeats} probes')


if __name__ == '__main__':
    main()
