"""Build Papers and Poppler from pinned source and verify PDF-scoped AFL++ edges.

Only the two repository valid controls are replayed; no mutation campaign runs.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
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

IMAGE = 'parsarium-afl/pdf-c-gnome-papers:local'
AFL_RELEASE = '4.33c-1.1ubuntu1'
PRELOAD = '/work/install/lib/papers/6/backends/libpdfdocument.so'
SANDBOX = ['--network', 'none', '--read-only', '--cap-drop', 'ALL',
           '--security-opt', 'no-new-privileges', '--user', f'{os.getuid()}:{os.getgid()}',
           '--tmpfs', '/tmp:rw,exec,nosuid,size=64m', '--workdir', '/tmp']


def call(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'{command[:6]} failed: {(result.stdout + result.stderr)[-3500:]}')
    return result.stdout.strip()


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def image_run(*args: str) -> str:
    return call(['docker', 'run', '--rm', '--platform', MANIFEST['platform'], *SANDBOX, *args])


def replay(path: Path) -> dict:
    return json.loads(image_run('-e', f'LD_PRELOAD={PRELOAD}',
                                '-v', f'{path}:/input/control:ro',
                                '--entrypoint', '/work/replay', IMAGE, '/input/control'))


def edge_ids(path: Path, map_size: int, directory: Path, label: str) -> set[str]:
    output = directory / f'{label}.map'
    probe = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                            *SANDBOX, '-e', f'AFL_MAP_SIZE={map_size}',
                            '-v', f'{path}:/input/control:ro',
                            '-v', f'{directory}:/coverage', '--entrypoint', 'afl-showmap',
                            IMAGE, '-e', '-m', 'none', '-t', '30000',
                            '-o', f'/coverage/{label}.map', '--',
                            '/work/replay', '/input/control'],
                           cwd=ROOT, capture_output=True, text=True)
    report = probe.stdout + probe.stderr
    if probe.returncode or not re.search(r'Captured \d+ tuples', report):
        raise RuntimeError(f'afl-showmap {label}: {report[-3500:]}')
    ids = {line.partition(':')[0] for line in output.read_text().splitlines() if line}
    output.unlink()
    return ids


def main() -> None:
    base = PROJECT / 'verification.json'
    if not base.is_file() or json.loads(base.read_text()).get('pass') is not True:
        raise RuntimeError('verified Papers PDF control is required')
    allowlist = (PROJECT / 'afl-allowlist.txt').read_text()
    for source in ('pps-poppler.c', 'poppler-document.cc', 'Parser.cc'):
        if f'src:{source}' not in allowlist:
            raise RuntimeError(f'PDF parser source absent from allowlist: {source}')
    dockerfile = OVERLAY / 'Dockerfile'
    source = (PROJECT / 'Dockerfile').read_text()
    if source.count('apt-get install -y --no-install-recommends') != 2:
        raise RuntimeError('Dockerfile apt shape changed')
    source = source.replace('apt-get install -y --no-install-recommends',
                            f'apt-get install -y --no-install-recommends afl++={AFL_RELEASE} python3')
    source = source.replace('ENV PKG_CONFIG_PATH=/work/install/lib/pkgconfig',
                            'ENV PKG_CONFIG_PATH=/work/install/lib/pkgconfig PARSARIUM_BUILD=afl')
    source += f'\nENV AFL_PRELOAD={PRELOAD}\n'
    dockerfile.write_text('# AFL++ PDF parser source overlay\n' + source)
    with docker_build_slot():
        call(['docker', 'build', '--quiet', '--platform', MANIFEST['platform'],
              '-f', str(dockerfile), '-t', IMAGE, str(PROJECT)])
    image_id = call(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}'])
    version = image_run('--entrypoint', 'dpkg-query', IMAGE, '-W', '-f=${Version}', 'afl++')
    if version != AFL_RELEASE:
        raise RuntimeError(f'AFL++ version mismatch: {version}')
    parser_modules = [PRELOAD, '/work/install/lib/libpoppler-glib.so',
                      '/work/install/lib/libpoppler.so']
    for module in parser_modules:
        symbols = image_run('--entrypoint', 'llvm-nm', IMAGE, '-D', module)
        if '__afl_area_ptr' not in symbols:
            raise RuntimeError(f'no AFL++ instrumentation in {module}')
    wrapper_symbols = image_run('--entrypoint', 'llvm-nm', IMAGE, '-D',
                                '/work/install/lib/libppsdocument-4.0.so')
    if '__afl_area_ptr' in wrapper_symbols:
        raise RuntimeError('AFL++ instrumentation leaked into Papers document wrapper')
    probe = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                            '-e', 'AFL_DUMP_MAP_SIZE=1', '-e', f'LD_PRELOAD={PRELOAD}',
                            '--entrypoint', '/work/replay', IMAGE],
                           cwd=ROOT, capture_output=True, text=True)
    sizes = re.findall(r'(?m)^\d+$', probe.stdout)
    # The no-input replay exits 2 after AFL prints the map size.
    if len(sizes) != 1:
        raise RuntimeError(f'AFL map size probe failed: {(probe.stdout + probe.stderr)[-2000:]}')
    map_size = int(sizes[0])
    control = ROOT / MANIFEST['control']
    variant = ROOT / 'controls/pdf/one-page.pdf'
    observed = replay(control)
    variant_observed = replay(variant)
    if observed != {'pages': 2} or variant_observed != {'pages': 1}:
        raise RuntimeError(f'valid PDF outputs changed: {observed} / {variant_observed}')
    with tempfile.TemporaryDirectory(prefix='parsarium-papers-pdf-afl-') as temporary:
        directory = Path(temporary)
        controls = [edge_ids(control, map_size, directory, f'control-{i}') for i in range(3)]
        variants = [edge_ids(variant, map_size, directory, f'variant-{i}') for i in range(2)]
    control_stable = set.intersection(*controls)
    control_union = set.union(*controls)
    variant_stable = set.intersection(*variants)
    variant_union = set.union(*variants)
    ratio = len(control_stable) / len(control_union) if control_union else 0
    control_only = control_stable - variant_union
    variant_only = variant_stable - control_union
    if len(control_stable) < 2 or ratio < 0.98 or not (control_only or variant_only):
        raise RuntimeError(f'Papers/Poppler parser map lacks stable differential feedback: '
                           f'{len(control_stable)}/{len(control_union)}, '
                           f'{len(control_only)} control-only, {len(variant_only)} variant-only')
    feedback = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_scope': 'AFL++ source allowlist restricted to Papers PDF backend and source-built Poppler GLib/core',
        'instrumented_parser_modules': parser_modules,
        'uninstrumented_document_wrapper': '/work/install/lib/libppsdocument-4.0.so',
        'afl_map_size': map_size, 'control_sha256': digest(control),
        'valid_variant': str(variant.relative_to(ROOT)), 'valid_variant_sha256': digest(variant),
        'control_repeat_edge_counts': [len(edges) for edges in controls],
        'control_stable_edge_ids': len(control_stable),
        'control_union_edge_ids': len(control_union),
        'control_stability_ratio': round(ratio, 6),
        'variant_repeat_edge_counts': [len(edges) for edges in variants],
        'variant_stable_edge_ids': len(variant_stable),
        'stable_control_only_edge_ids': len(control_only),
        'stable_variant_only_edge_ids': len(variant_only),
        'control_output': observed, 'variant_output': variant_observed,
        'mutation_campaign_run': False,
    }
    feedback_file = OVERLAY / 'feedback-validation.json'
    feedback_file.write_text(json.dumps(feedback, indent=2) + '\n')
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'papers_poppler_pdf_source_scoped_afl_edges',
        'feedback_scope': feedback['feedback_scope'],
        'base_project_receipt_sha256': digest(base),
        'source_sha256': MANIFEST['source_sha256'],
        'underlying_source_sha256': MANIFEST['underlying_source_sha256'],
        'control_sha256': MANIFEST['control_sha256'],
        'image_id': image_id, 'platform': MANIFEST['platform'],
        'afl_package': version, 'afl_version_output': version,
        'afl_map_size': map_size, 'afl_entrypoint': '/work/replay',
        'afl_file_input': True, 'feedback_edges': len(controls[0]),
        'overlay_file_sha256': {name: digest(OVERLAY / name)
                                for name in ('Dockerfile', 'build.py', 'feedback-validation.json')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {len(controls[0])} PDF AFL++ edges; '
          f'{ratio:.4%} control stability; {len(control_only)} control-only, '
          f'{len(variant_only)} variant-only edges')


if __name__ == '__main__':
    main()
