"""Verify pdf_oxide-crate AFL++ pcguard feedback through the C++17 facade.

This reuses the base project's tagged-source Dockerfile with its AFL build
argument: the same pdf_oxide 0.3.78 archive, Cargo.lock and Rust 1.92.0
toolchain. Only the pdf_oxide crate carries pcguard instrumentation; its
dependency crates and the C++ harness objects must have none. Stable rustc's
sancov-module pass takes no source allowlist, so guards span the whole crate,
not only its lexer/parser/xref modules. Only fixed, valid PDFs are replayed;
no campaign is run.
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

IMAGE = f'parsarium-afl/{RELATIVE.parts[0]}-{RELATIVE.parts[1]}-{RELATIVE.parts[2]}:local'
AFL_RELEASE = '4.33c-1.1ubuntu1'
VARIANT = OVERLAY / 'valid-objstm.pdf'
VARIANT_OUTPUT = {'pages': 3}
SCOPE = ('pdf_oxide 0.3.78 Rust crate only (whole crate; stable rustc sancov-module has '
         'no per-file allowlist); dependency crates and C++17 harness uninstrumented')
SANDBOX = ['--network', 'none', '--read-only', '--cap-drop', 'ALL',
           '--security-opt', 'no-new-privileges', '--user', f'{os.getuid()}:{os.getgid()}',
           '--tmpfs', '/tmp:rw,exec,nosuid,size=64m', '--workdir', '/tmp']


def call(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'{command[:6]} failed: {(result.stdout + result.stderr)[-3000:]}')
    return result.stdout.strip()


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def image_run(*args: str) -> str:
    return call(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                 *SANDBOX, *args])


def replay(path: Path) -> dict:
    return json.loads(image_run('-v', f'{path}:/input/control:ro',
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
    if probe.returncode or not re.search(r'Captured \d+ tuples', probe.stdout + probe.stderr):
        raise RuntimeError(f'afl-showmap {label}: {(probe.stdout + probe.stderr)[-3000:]}')
    ids = {line.partition(':')[0] for line in output.read_text().splitlines() if line}
    output.unlink()
    return ids


def section_slots(object_path: str) -> int:
    sections = image_run('--entrypoint', 'llvm-readelf', IMAGE, '-SW', object_path)
    match = re.search(r'__sancov_guards\s+PROGBITS\s+\S+\s+\S+\s+([0-9A-Fa-f]+)\s', sections)
    return int(match.group(1), 16) // 4 if match else 0


def main() -> None:
    base = PROJECT / 'verification.json'
    if not base.is_file() or json.loads(base.read_text()).get('pass') is not True:
        raise RuntimeError('verified pdf_oxide C++ base project is required')
    dockerfile = OVERLAY / 'Dockerfile'
    shutil.copyfile(PROJECT / 'Dockerfile', dockerfile)
    with docker_build_slot():
        call(['docker', 'build', '--quiet', '--platform', MANIFEST['platform'],
              '--build-arg', 'PARSARIUM_BUILD=afl', '-f', str(dockerfile),
              '-t', IMAGE, str(PROJECT)])
    image_id = call(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}'])
    version = image_run('--entrypoint', 'dpkg-query', IMAGE, '-W', '-f=${Version}', 'afl++')
    if version != AFL_RELEASE:
        raise RuntimeError(f'AFL++ version mismatch: {version}')
    library_slots = section_slots('/work/libpdf_oxide.so')
    harness_slots = section_slots('/work/replay')
    if library_slots < 2 or harness_slots:
        raise RuntimeError(f'pcguard scope mismatch: pdf_oxide={library_slots}, harness={harness_slots}')
    control = ROOT / MANIFEST['control']
    second = PROJECT / MANIFEST['second_control']
    observed = replay(control)
    if observed != MANIFEST['expected_output']:
        raise RuntimeError(f'AFL control changed: {observed}')
    second_observed = replay(second)
    if second_observed != MANIFEST['second_control_expected_output']:
        raise RuntimeError(f'second valid PDF changed: {second_observed}')
    variant_observed = replay(VARIANT)
    if variant_observed != VARIANT_OUTPUT:
        raise RuntimeError(f'valid object-stream PDF was not parsed: {variant_observed}')
    map_probe = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                                *SANDBOX, '-e', 'AFL_DUMP_MAP_SIZE=1',
                                '--entrypoint', '/work/replay', IMAGE],
                               cwd=ROOT, capture_output=True, text=True)
    # AFL prints the map size and exits before application argument handling.
    map_text = map_probe.stdout.strip()
    if not map_text.isdigit():
        raise RuntimeError(f'AFL map size probe failed: {map_text}')
    map_size = int(map_text)
    with tempfile.TemporaryDirectory(prefix='parsarium-pdf-oxide-cpp-afl-') as temporary:
        directory = Path(temporary)
        controls = [edge_ids(control, map_size, directory, f'control-{i}') for i in range(3)]
        seconds = [edge_ids(second, map_size, directory, f'second-{i}') for i in range(2)]
        variants = [edge_ids(VARIANT, map_size, directory, f'variant-{i}') for i in range(2)]
    control_stable = set.intersection(*controls)
    control_union = set.union(*controls)
    second_stable = set.intersection(*seconds)
    variant_stable = set.intersection(*variants)
    if len(control_stable) < 2 or len(variant_stable - control_union) < 1:
        raise RuntimeError('pdf_oxide pcguard map lacks repeat-stable, variant-sensitive edges')
    ratio = len(control_stable) / len(control_union)
    if ratio < 0.99:
        raise RuntimeError(f'control edge stability too low: {ratio:.4f}')
    feedback = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_scope': SCOPE,
        'pdf_oxide_guard_slots': library_slots, 'harness_guard_slots': harness_slots,
        'afl_map_size': map_size, 'control_sha256': digest(control),
        'second_valid_input': str(second.relative_to(ROOT)),
        'second_valid_input_sha256': digest(second),
        'valid_variant': str(VARIANT.relative_to(ROOT)), 'valid_variant_sha256': digest(VARIANT),
        'control_repeat_edge_counts': [len(edges) for edges in controls],
        'control_stable_edge_ids': len(control_stable),
        'control_union_edge_ids': len(control_union),
        'control_stability_ratio': round(ratio, 6),
        'second_repeat_edge_counts': [len(edges) for edges in seconds],
        'stable_second_only_edge_ids': len(second_stable - control_union),
        'variant_repeat_edge_counts': [len(edges) for edges in variants],
        'variant_stable_edge_ids': len(variant_stable),
        'stable_variant_only_edge_ids': len(variant_stable - control_union),
        'control_output': observed, 'second_output': second_observed,
        'variant_output': variant_observed, 'mutation_campaign_run': False,
    }
    feedback_file = OVERLAY / 'feedback-validation.json'
    feedback_file.write_text(json.dumps(feedback, indent=2) + '\n')
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'pdf_oxide_rust_crate_pcguard_edges',
        'shared_parser_family': MANIFEST['shared_parser_family'],
        'shared_parser_family_projects': MANIFEST['shared_parser_family_projects'],
        'feedback_scope': SCOPE,
        'base_project_receipt_sha256': digest(base),
        'source_sha256': MANIFEST['source_sha256'],
        'control_sha256': MANIFEST['control_sha256'],
        'image_id': image_id, 'platform': MANIFEST['platform'],
        'afl_package': version, 'afl_version_output': version,
        'afl_map_size': map_size, 'afl_entrypoint': '/work/replay',
        'afl_file_input': True, 'feedback_edges': len(controls[0]),
        'feedback_validation_sha256': digest(feedback_file),
        'overlay_file_sha256': {name: digest(OVERLAY / name)
                                for name in ('Dockerfile', 'build.py', 'make_variant.py',
                                             'valid-objstm.pdf', 'feedback-validation.json')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {len(controls[0])} pdf_oxide AFL++ edges; '
          f'{ratio:.4%} control stability; {len(variant_stable - control_union)} variant-only edges')


if __name__ == '__main__':
    main()
