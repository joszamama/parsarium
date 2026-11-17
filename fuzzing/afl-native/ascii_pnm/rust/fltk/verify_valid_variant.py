"""Compare native FLTK PNM source and AFL++ feedback on two valid controls."""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[5]
OVERLAY = Path(__file__).resolve().parent
CONTROL = ROOT / 'controls/ascii_pnm/red-green.ppm'
VARIANT = ROOT / 'controls/ascii_pnm/black-white.pgm'
BASE = 'parsarium/ascii_pnm-rust-fltk:local'
AFL = 'parsarium-afl/ascii_pnm-rust-fltk:local'


def run(args: list[str], data: bytes | None = None) -> str:
    result = subprocess.run(args, input=data, capture_output=True, timeout=90)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr).decode(errors='replace')[-2000:])
    return result.stdout.decode(errors='replace')


def sandbox(*args: str, stdin: bool = False) -> list[str]:
    return ['docker', 'run', '--rm', *(['-i'] if stdin else []),
            '--platform', 'linux/arm64', '--network', 'none', '--read-only',
            '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
            '--user', f'{os.getuid()}:{os.getgid()}',
            '--tmpfs', '/tmp:rw,exec,nosuid,size=64m', '--workdir', '/tmp', *args]


def native_features(sample: Path, label: str, work: Path) -> tuple[dict, set[tuple]]:
    output = run(sandbox('-e', f'LLVM_PROFILE_FILE=/coverage/{label}-%m.profraw',
                         '-v', f'{sample}:/input/case:ro', '-v', f'{work}:/coverage',
                         '--entrypoint', '/work/replay', BASE, '/input/case'))
    raws = sorted(work.glob(f'{label}-*.profraw'))
    if not raws:
        raise RuntimeError('FLTK native profile absent')
    run(sandbox('-v', f'{work}:/coverage', '--entrypoint', '/work/llvm-profdata',
                BASE, 'merge', *(f'/coverage/{p.name}' for p in raws),
                '-o', f'/coverage/{label}.profdata'))
    report = json.loads(run(sandbox('-v', f'{work}:/coverage:ro',
                                    '--entrypoint', '/work/llvm-cov', BASE,
                                    'export', '/work/replay',
                                    f'-instr-profile=/coverage/{label}.profdata')))
    features = set()
    for source in report['data'][0]['files']:
        if source['filename'].endswith('/Fl_PNM_Image.cxx'):
            features.update((line, column) for line, column, count, has_count,
                            region_start, *_ in source['segments']
                            if has_count and region_start and count > 0)
    if not features:
        raise RuntimeError('FLTK PNM loader source coverage absent')
    return json.loads(output), features


def afl_map(data: bytes, label: str, repeat: int, work: Path, map_size: int) -> set[str]:
    run(sandbox('-e', f'AFL_MAP_SIZE={map_size}', '-v', f'{work}:/coverage',
                '--entrypoint', 'afl-showmap', AFL, '-m', 'none', '-t', '10000',
                '-o', f'/coverage/{label}-{repeat}.map', '--', '/work/afl_fuzzer',
                stdin=True), data)
    return {line.split(':', 1)[0] for line in
            (work / f'{label}-{repeat}.map').read_text().splitlines() if line}


def main() -> None:
    base_receipt = json.loads((ROOT / 'projects/ascii_pnm/rust/fltk/verification.json').read_text())
    overlay_path = OVERLAY / 'verification.json'
    overlay = json.loads(overlay_path.read_text())
    for image, expected in ((BASE, base_receipt['image_id']), (AFL, overlay['image_id'])):
        actual = run(['docker', 'image', 'inspect', image, '--format', '{{.Id}}']).strip()
        if actual != expected:
            raise RuntimeError(f'{image}: image differs from receipt')
    if sha256(CONTROL.read_bytes()).hexdigest() != overlay['control_sha256']:
        raise RuntimeError('control changed')
    with tempfile.TemporaryDirectory(prefix='parsarium-fltk-pnm-valid-') as temporary:
        work = Path(temporary)
        control_output, control_source = native_features(CONTROL, 'control', work)
        variant_output, variant_source = native_features(VARIANT, 'variant', work)
        if control_output != {'width': 2, 'height': 1,
                              'rgb': [255, 0, 0, 0, 255, 0]}:
            raise RuntimeError('control output changed')
        if variant_output != {'width': 2, 'height': 1, 'rgb': [0, 255]}:
            raise RuntimeError(f'valid PGM result changed: {variant_output}')
        native_delta = variant_source - control_source
        if not native_delta:
            raise RuntimeError('valid PGM adds no FLTK PNM parser regions')
        control_maps = [afl_map(CONTROL.read_bytes(), 'control', i, work,
                                overlay['afl_map_size']) for i in range(3)]
        variant_maps = [afl_map(VARIANT.read_bytes(), 'variant', i, work,
                                overlay['afl_map_size']) for i in range(3)]
        edge_delta = set.intersection(*variant_maps) - set.union(*control_maps)
        if not edge_delta:
            raise RuntimeError('valid PGM adds no stable AFL++ feedback')
    receipt = {
        'schema_version': 1, 'project': 'ascii_pnm/rust/fltk', 'pass': True,
        'base_receipt_sha256': sha256((ROOT / 'projects/ascii_pnm/rust/fltk/verification.json').read_bytes()).hexdigest(),
        'overlay_receipt_sha256': sha256(overlay_path.read_bytes()).hexdigest(),
        'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'control_sha256': sha256(CONTROL.read_bytes()).hexdigest(),
        'variant_sha256': sha256(VARIANT.read_bytes()).hexdigest(),
        'variant_output': variant_output,
        'control_native_pnm_regions': len(control_source),
        'variant_native_pnm_regions': len(variant_source),
        'variant_only_native_pnm_regions': len(native_delta),
        'control_afl_repeats': [len(x) for x in control_maps],
        'variant_afl_repeats': [len(x) for x in variant_maps],
        'stable_variant_only_afl_edges': len(edge_delta),
    }
    (OVERLAY / 'valid-variant.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified valid PGM: {len(native_delta)} new native PNM regions, '
          f'{len(edge_delta)} stable new AFL++ edges')


if __name__ == '__main__':
    main()
