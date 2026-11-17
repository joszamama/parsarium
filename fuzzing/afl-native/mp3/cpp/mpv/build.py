"""Build and verify AFL++ feedback from FFmpeg's tagged-MP3 parser behind libmpv.

The call site is the C++17 harness of projects/mp3/cpp/mpv.

The overlay rebuilds the pinned mpv 0.42.0, FFmpeg 9.0.2 and libplacebo
7.387.0 sources with the same configuration as the base project
(PARSARIUM_BUILD=afl). AFL++'s allowlist limits pcguard instrumentation to
FFmpeg's ID3v2 and ID3v1 readers (libavformat/id3v2.c, id3v1.c), its MP3
demuxer (mp3dec.c) and the helpers mp3dec.c calls (replaygain.c,
libavcodec/mpegaudiodecheader.c and the mpegaudio_parser.c frame parser), plus
mpv's libavformat wrapper (demux/demux_lavf.c); build.sh fails if any other
archive member or the C++ harness objects carry guards. Every tuple that
afl-showmap reports therefore comes from those sources.

The control (ID3v2.3) and a valid variant with the same audio frames under an
ID3v2.4 tag (the project's valid-v24.mp3, a copy of
controls/mp3/id3v2-tagged-tone-v24.mp3) must give the exact expected output in
the AFL++ build, give the same tuples on every repeated probe, and the variant
must add tuples absent from the control. The verified source-coverage image of the base project
replays both files over the same sources and must show variant-only regions in
FFmpeg's id3v2.c, so the feedback difference follows the parsed tag.

Each input is probed --repeats times (default 3). No campaign is started.
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
SLUG = '-'.join(RELATIVE.parts)
IMAGE = f'parsarium-afl/{SLUG}:local'
BASE_IMAGE = f'parsarium/{SLUG}:local'
AFL_RELEASE = '4.33c-1.1ubuntu1'
SANDBOX = ['--network', 'none', '--read-only', '--cap-drop', 'ALL',
           '--security-opt', 'no-new-privileges', '--user', f'{os.getuid()}:{os.getgid()}',
           '--tmpfs', '/tmp:rw,exec,nosuid,size=64m', '--workdir', '/tmp']
ALLOWLIST = ['src: id3v2.c', 'src: mp3dec.c',
             'src: id3v1.c', 'src: replaygain.c',
             'src: mpegaudiodecheader.c', 'src: mpegaudio_parser.c',
             'src: *demux/demux_lavf.c']
GUARDED = re.compile(r'libavformat\.a\((id3v2|mp3dec|id3v1|replaygain)\.o\)$'
                     r'|libavcodec\.a\((mpegaudiodecheader|mpegaudio_parser)\.o\)$'
                     r'|libmpv\.a\(.*demux_lavf\.c\.o\)$')
REQUIRED_GUARDED = [re.compile(p) for p in (
    r'libavformat\.a\(id3v2\.o\)$', r'libavformat\.a\(mp3dec\.o\)$',
    r'libavformat\.a\(id3v1\.o\)$', r'libavformat\.a\(replaygain\.o\)$',
    r'libavcodec\.a\(mpegaudiodecheader\.o\)$', r'libavcodec\.a\(mpegaudio_parser\.o\)$',
    r'libmpv\.a\(.*demux_lavf\.c\.o\)$')]
# The same sources in the base project's LLVM source coverage.
ID3V2 = '/work/ffmpeg/libavformat/id3v2.c'
MP3DEC = '/work/ffmpeg/libavformat/mp3dec.c'
DEMUX_LAVF = '/work/source/demux/demux_lavf.c'
SCOPE = (ID3V2, MP3DEC, '/work/ffmpeg/libavformat/id3v1.c',
         '/work/ffmpeg/libavformat/replaygain.c',
         '/work/ffmpeg/libavcodec/mpegaudiodecheader.c',
         '/work/ffmpeg/libavcodec/mpegaudio_parser.c', DEMUX_LAVF)


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'{command[:5]} failed: {(result.stdout + result.stderr)[-3000:]}')
    return result.stdout.strip()


def docker(image: str, entrypoint: str, options: list[str], arguments: list[str]) -> list[str]:
    return ['docker', 'run', '--rm', '--platform', MANIFEST['platform'], *SANDBOX,
            *options, '--entrypoint', entrypoint, image, *arguments]


def replay(sample: Path) -> dict:
    return json.loads(run(docker(IMAGE, '/work/replay',
                                 ['-v', f'{sample}:/input/sample:ro'], ['/input/sample'])))


def showmap(map_size: int, sample: Path) -> set[str]:
    with tempfile.TemporaryDirectory(prefix='parsarium-mpv-cpp-mp3-afl-') as temporary:
        result = subprocess.run(docker(
            IMAGE, 'afl-showmap', ['-e', f'AFL_MAP_SIZE={map_size}',
            '-v', f'{sample}:/input/sample:ro', '-v', f'{temporary}:/coverage'],
            ['-m', 'none', '-t', '30000', '-o', '/coverage/edges.txt', '--',
             '/work/fuzzer', '/input/sample']), cwd=ROOT, capture_output=True, text=True)
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


def source_regions(sample: Path, label: str) -> tuple[dict, set[tuple]]:
    """Replay one file in the verified base coverage image; return its output and
    the executed region starts in the allowlisted sources."""
    with tempfile.TemporaryDirectory(prefix='parsarium-mpv-cpp-mp3-src-') as temporary:
        work = Path(temporary)
        output = json.loads(run(docker(
            BASE_IMAGE, '/work/replay', ['-e', f'LLVM_PROFILE_FILE=/coverage/{label}-%m.profraw',
            '-v', f'{sample}:/input/sample:ro', '-v', f'{work}:/coverage'], ['/input/sample'])))
        raws = sorted(work.glob(f'{label}-*.profraw'))
        if not raws:
            raise RuntimeError(f'{label}: source profile absent')
        run(docker(BASE_IMAGE, 'llvm-profdata', ['-v', f'{work}:/coverage'],
                   ['merge', '-sparse', *(f'/coverage/{p.name}' for p in raws),
                    '-o', f'/coverage/{label}.profdata']))
        report = json.loads(run(docker(BASE_IMAGE, 'llvm-cov', ['-v', f'{work}:/coverage:ro'],
                                       ['export', '/work/replay',
                                        f'-instr-profile=/coverage/{label}.profdata'])))
    regions = set()
    for source in report['data'][0]['files']:
        if source['filename'] in SCOPE:
            regions.update((source['filename'], line, column)
                           for line, column, count, has_count, region_start, *_
                           in source['segments'] if has_count and region_start and count > 0)
    for required in (ID3V2, MP3DEC, DEMUX_LAVF):
        if not any(r[0] == required for r in regions):
            raise RuntimeError(f'{label}: no source coverage in {required}')
    return output, regions


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--repeats', type=int, default=3,
                     help='afl-showmap probes per input for stability (minimum 2)')
    args = cli.parse_args()
    if args.repeats < 2:
        raise SystemExit('--repeats must be at least 2')
    base_receipt = PROJECT / 'verification.json'
    if not base_receipt.is_file() or not json.loads(base_receipt.read_text()).get('pass'):
        raise RuntimeError('base mpv C++ MP3 project must be verified first')
    base_image_id = run(['docker', 'image', 'inspect', BASE_IMAGE, '--format', '{{.Id}}'])
    if base_image_id != json.loads(base_receipt.read_text())['image_id']:
        raise RuntimeError('base coverage image differs from the verified project')
    control = ROOT / MANIFEST['control']
    variant = PROJECT / MANIFEST['valid_variant']
    control_hash = sha256(control.read_bytes()).hexdigest()
    variant_hash = sha256(variant.read_bytes()).hexdigest()
    if control_hash != MANIFEST['control_sha256']:
        raise RuntimeError('control differs from its manifest hash')
    if variant_hash != MANIFEST['valid_variant_sha256']:
        raise RuntimeError('valid ID3v2.4 variant differs from its manifest hash')
    if sha256((ROOT / MANIFEST['valid_variant_source']).read_bytes()).hexdigest() != variant_hash:
        raise RuntimeError('valid ID3v2.4 variant differs from its control source')
    expected, variant_expected = MANIFEST['expected_output'], MANIFEST['valid_variant_expected_output']

    with docker_build_slot():
        run(['docker', 'build', '--quiet', '--platform', MANIFEST['platform'],
             '-f', str(OVERLAY / 'Dockerfile'), '-t', IMAGE, str(PROJECT)])
    image_id = run(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}'])
    version = run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                   '--entrypoint', 'dpkg-query', IMAGE, '-W', '-f=${Version}', 'afl++'])
    if version != AFL_RELEASE:
        raise RuntimeError(f'AFL++ version mismatch: {version}')

    # Archive guard evidence recorded by build.sh inside the image.
    allowlist = run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                     '--entrypoint', 'cat', IMAGE, '/work/afl-allowlist.txt']).splitlines()
    if allowlist != ALLOWLIST:
        raise RuntimeError(f'AFL++ allowlist differs: {allowlist}')
    guarded = sorted(line.rpartition('/')[2] for line in run(
        ['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
         '--entrypoint', 'cat', IMAGE, '/work/afl-guarded.txt']).splitlines() if line)
    if not guarded or not all(GUARDED.search(member) for member in guarded):
        raise RuntimeError(f'AFL++ guards outside the tagged-MP3 parser sources: {guarded}')
    missing = [p.pattern for p in REQUIRED_GUARDED if not any(p.search(m) for m in guarded)]
    if missing:
        raise RuntimeError(f'AFL++ guards absent from allowlisted members: {missing}')

    # Exact output from the AFL++-instrumented build.
    observed = replay(control)
    if observed != expected:
        raise RuntimeError(f'AFL-instrumented build changed control result: {observed}')
    variant_output = replay(variant)
    if variant_output != variant_expected:
        raise RuntimeError(f'valid ID3v2.4 variant parsed unexpectedly: {variant_output}')

    # Repeated AFL++ maps.
    probe = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                            '-e', 'AFL_DUMP_MAP_SIZE=1', '--entrypoint', '/work/fuzzer', IMAGE],
                           cwd=ROOT, capture_output=True, text=True)
    if not probe.stdout.strip().isdigit():
        raise RuntimeError(f'AFL++ map size probe failed: {probe.stderr[-2000:]}')
    map_size = int(probe.stdout.strip())
    control_maps = [showmap(map_size, control) for _ in range(args.repeats)]
    variant_maps = [showmap(map_size, variant) for _ in range(args.repeats)]
    control_stability, variant_stability = stability(control_maps), stability(variant_maps)
    if not control_stability['all_repeats_identical']:
        raise RuntimeError(f'control AFL++ maps differ across repeats: {control_stability}')
    if not variant_stability['all_repeats_identical']:
        raise RuntimeError(f'variant AFL++ maps differ across repeats: {variant_stability}')
    control_edges, variant_edges = control_maps[0], variant_maps[0]
    if len(control_edges) < 2:
        raise RuntimeError(f'insufficient tagged-MP3 AFL++ feedback: {len(control_edges)} edges')
    if not variant_edges - control_edges:
        raise RuntimeError('valid ID3v2.4 variant produced no new tagged-MP3 AFL++ feedback')

    # Source differential over the same sources in the verified coverage image.
    source_output, control_regions = source_regions(control, 'control')
    source_variant_output, variant_regions = source_regions(variant, 'variant')
    if source_output != expected or source_variant_output != variant_expected:
        raise RuntimeError(f'coverage build parsed unexpectedly: {source_output}, {source_variant_output}')
    variant_only = variant_regions - control_regions
    id3v2_only = {r for r in variant_only if r[0] == ID3V2}
    if not id3v2_only:
        raise RuntimeError('valid ID3v2.4 variant adds no FFmpeg id3v2.c source regions')

    def by_file(regions: set[tuple]) -> dict:
        return {name: sum(r[0] == name for r in regions) for name in SCOPE}

    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'ffmpeg_tagged_mp3_mpv_demux_lavf_pcguard_edges',
        'feedback_scope': 'FFmpeg 9.0.2 libavformat/id3v2.c, mp3dec.c, id3v1.c, replaygain.c, libavcodec/mpegaudiodecheader.c, mpegaudio_parser.c and mpv 0.42.0 demux/demux_lavf.c via AFL++ allowlist; the rest of libmpv, libavformat, libavcodec, libplacebo and the C++17 harness uninstrumented',
        'afl_allowlist': allowlist,
        'afl_guarded_archive_members': guarded,
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'base_image_id': base_image_id,
        'source_sha256': MANIFEST['source_sha256'],
        'underlying_source_sha256': MANIFEST['underlying_source_sha256'],
        'control_sha256': control_hash,
        'variant_sha256': variant_hash,
        'control_output': observed,
        'variant_output': variant_output,
        'image_id': image_id, 'platform': MANIFEST['platform'],
        'afl_package': version, 'afl_version_output': version,
        'afl_file_input': True,
        'afl_map_size': map_size,
        'repeats': args.repeats,
        'feedback_edges': len(control_edges),
        'variant_feedback_edges': len(variant_edges),
        'edges_only_in_control': len(control_edges - variant_edges),
        'edges_only_in_variant': len(variant_edges - control_edges),
        'control_stability': control_stability,
        'variant_stability': variant_stability,
        'source_differential': {
            'image_id': base_image_id,
            'control_regions': by_file(control_regions),
            'variant_regions': by_file(variant_regions),
            'variant_only_regions': by_file(variant_only),
            'control_only_regions': by_file(control_regions - variant_regions),
        },
        'overlay_file_sha256': {
            name: sha256((OVERLAY / name).read_bytes()).hexdigest()
            for name in ('Dockerfile', 'build.py')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {len(control_edges)} tagged-MP3 AFL++ feedback edges, '
          f'{receipt["edges_only_in_variant"]} edges only in the ID3v2.4 variant, '
          f'{len(id3v2_only)} variant-only id3v2.c regions, '
          f'identical maps over {args.repeats} probes')


if __name__ == '__main__':
    main()
