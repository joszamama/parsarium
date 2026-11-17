"""Check VLC tagged-MP3 parser-source and AFL++ feedback on two valid files.

The control has an ID3v2.3 tag; the variant carries the same MPEG audio
frames under an ID3v2.4 tag with synchsafe frame sizes and UTF-8 text, so the
difference exercises the ID3v2 parsers rather than the audio path.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[5]
OVERLAY = Path(__file__).resolve().parent
IMAGE = 'parsarium-afl/mp3-c-vlc:local'
CONTROL = ROOT / 'controls/mp3/id3v2-tagged-tone.mp3'
VARIANT = ROOT / 'controls/mp3/id3v2-tagged-tone-v24.mp3'
VLC = '/work/source/modules/'
# Parsing code only: the libVLC wrapper, file access and TagLib plugin glue
# (meta_engine/taglib.cpp) are excluded.
VLC_PARSERS = tuple(VLC + name for name in (
    'stream_filter/skiptags.c', 'demux/mpeg/es.c', 'packetizer/mpegaudio.c',
    'meta_engine/ID3Tag.h', 'meta_engine/ID3Meta.h', 'meta_engine/ID3Text.h'))
VLC_ID3 = tuple(VLC + 'meta_engine/ID3' + name for name in ('Tag.h', 'Meta.h', 'Text.h'))
TAGLIB = '/work/taglib-1.13.1/taglib/'
TAGLIB_ID3V2 = TAGLIB + 'mpeg/id3v2/'
EXPECTED = {'title': 'Parsarium', 'audio_tracks': 1, 'mp3_tracks': 1,
            'audio_codec': 'mp3 ', 'rate': 8000, 'channels': 1}


def run(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=90)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])
    return result.stdout


def sandbox(*args: str) -> list[str]:
    return ['docker', 'run', '--rm', '--platform', 'linux/arm64', '--network', 'none',
            '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
            '--user', f'{os.getuid()}:{os.getgid()}',
            '--tmpfs', '/tmp:rw,exec,nosuid,size=64m', '--workdir', '/tmp', *args]


def source_features(sample: Path, label: str, work: Path) -> tuple[dict, set[tuple]]:
    output = run(sandbox('-e', f'LLVM_PROFILE_FILE=/coverage/{label}-%m.profraw',
                         '-v', f'{sample}:/input/case:ro', '-v', f'{work}:/coverage',
                         '--entrypoint', '/work/replay', IMAGE, '/input/case'))
    raws = sorted(work.glob(f'{label}-*.profraw'))
    if not raws:
        raise RuntimeError(f'{label}: native VLC profile absent')
    run(sandbox('-v', f'{work}:/coverage', '--entrypoint', 'llvm-profdata', IMAGE,
                'merge', *(f'/coverage/{p.name}' for p in raws),
                '-o', f'/coverage/{label}.profdata'))
    report = json.loads(run(sandbox('-v', f'{work}:/coverage:ro',
                                    '--entrypoint', 'llvm-cov', IMAGE, 'export',
                                    '/work/replay',
                                    f'-instr-profile=/coverage/{label}.profdata')))
    features = set()
    for source in report['data'][0]['files']:
        filename = source['filename']
        if filename in VLC_PARSERS or filename.startswith(TAGLIB):
            features.update((filename, line, column)
                            for line, column, count, has_count, region_start, *_
                            in source['segments'] if has_count and region_start and count > 0)
    if not any(f[0] in VLC_ID3 for f in features) or \
            not any(f[0].startswith(TAGLIB_ID3V2) for f in features):
        raise RuntimeError(f'{label}: VLC or TagLib ID3v2 source coverage absent')
    return json.loads(output), features


def afl_map(sample: Path, label: str, work: Path, map_size: int, repeat: int) -> set[str]:
    destination = f'/coverage/{label}-{repeat}.map'
    run(sandbox('-e', f'AFL_MAP_SIZE={map_size}',
                '-v', f'{sample}:/input/case:ro', '-v', f'{work}:/coverage',
                '--entrypoint', 'afl-showmap', IMAGE, '-m', 'none', '-t', '10000',
                '-o', destination, '--', '/work/fuzzer', '/input/case'))
    return {line.split(':', 1)[0] for line in
            (work / f'{label}-{repeat}.map').read_text().splitlines() if line}


def main() -> None:
    overlay_receipt = json.loads((OVERLAY / 'verification.json').read_text())
    image_id = run(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}']).strip()
    if not overlay_receipt['pass'] or image_id != overlay_receipt['image_id']:
        raise RuntimeError('AFL++ image differs from verified overlay')
    if sha256(CONTROL.read_bytes()).hexdigest() != overlay_receipt['control_sha256']:
        raise RuntimeError('control changed')
    with tempfile.TemporaryDirectory(prefix='parsarium-vlc-mp3-valid-') as temporary:
        work = Path(temporary)
        control_output, control_source = source_features(CONTROL, 'control', work)
        variant_output, variant_source = source_features(VARIANT, 'variant', work)
        if control_output != EXPECTED:
            raise RuntimeError(f'control parsed unexpectedly: {control_output}')
        if variant_output != EXPECTED:
            raise RuntimeError(f'valid variant parsed unexpectedly: {variant_output}')
        source_delta = variant_source - control_source
        vlc_id3_delta = {f for f in source_delta if f[0] in VLC_ID3}
        taglib_id3v2_delta = {f for f in source_delta if f[0].startswith(TAGLIB_ID3V2)}
        if not vlc_id3_delta and not taglib_id3v2_delta:
            raise RuntimeError('valid variant adds no VLC or TagLib ID3v2 parser regions')
        control_maps = [afl_map(CONTROL, 'control', work,
                                overlay_receipt['afl_map_size'], i) for i in range(3)]
        variant_maps = [afl_map(VARIANT, 'variant', work,
                                overlay_receipt['afl_map_size'], i) for i in range(3)]
        stable_variant_only = set.intersection(*variant_maps) - set.union(*control_maps)
        if not stable_variant_only:
            raise RuntimeError('valid variant adds no stable AFL++ feedback')
    receipt = {
        'schema_version': 1, 'project': 'mp3/c/vlc', 'pass': True,
        'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
        'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'control_sha256': sha256(CONTROL.read_bytes()).hexdigest(),
        'variant_sha256': sha256(VARIANT.read_bytes()).hexdigest(),
        'variant_output': variant_output,
        'control_parser_source_regions': len(control_source),
        'variant_parser_source_regions': len(variant_source),
        'variant_only_parser_source_regions': len(source_delta),
        'variant_only_vlc_id3v2_regions': len(vlc_id3_delta),
        'variant_only_taglib_id3v2_regions': len(taglib_id3v2_delta),
        'control_afl_repeats': [len(x) for x in control_maps],
        'variant_afl_repeats': [len(x) for x in variant_maps],
        'stable_variant_only_afl_edges': len(stable_variant_only),
    }
    (OVERLAY / 'valid-variant.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified valid ID3v2.4 variant: {len(vlc_id3_delta)} new VLC ID3v2 regions, '
          f'{len(taglib_id3v2_delta)} new TagLib ID3v2 regions, '
          f'{len(stable_variant_only)} stable new AFL++ edges')


if __name__ == '__main__':
    main()
