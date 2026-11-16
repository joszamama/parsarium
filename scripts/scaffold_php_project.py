"""Stage one Composer parser as a pinned PHP/Xdebug container candidate."""

import argparse
import fcntl
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "projects/png/php/marc1706_fast_image_size"
BASE_IMAGE = "ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96"
CACHE = Path(tempfile.gettempdir()) / "parsarium-php-augmented-locks"


def augmented_lock(lock_path: Path) -> Path:
    original = lock_path.with_name("composer.json")
    if not original.is_file():
        raise ValueError(f"missing Composer manifest for {lock_path}")
    key = sha256(original.read_bytes() + lock_path.read_bytes()).hexdigest()
    directory = CACHE / key
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".lock").open("w") as guard:
        fcntl.flock(guard, fcntl.LOCK_EX)
        cached = directory / "composer.lock"
        if (not cached.exists() or not any(item["name"] == "nikic/php-fuzzer"
                                             for item in json.loads(cached.read_text())["packages"])):
            shutil.copyfile(original, directory / "composer.json")
            shutil.copyfile(lock_path, directory / "composer.lock")
            updated = subprocess.run(
                ["composer", "require", "nikic/php-fuzzer:v0.0.11",
                 "--no-install", "--no-interaction", "--no-progress", "--no-audit", "--ignore-platform-reqs"],
                cwd=directory, capture_output=True, text=True, timeout=180)
            if updated.returncode:
                raise RuntimeError(f"Composer lock update failed: {updated.stderr[-1000:]}")
    return directory


def release_archive(dist_url: str) -> tuple[str, str]:
    match = re.fullmatch(r"https://api\.github\.com/repos/([^/]+)/([^/]+)/zipball/([^/?]+)", dist_url)
    if match:
        url = f"https://codeload.github.com/{match[1]}/{match[2]}/legacy.zip/{match[3]}"
    else:
        url = dist_url
    with urllib.request.urlopen(url, timeout=60) as response:
        digest = sha256(response.read()).hexdigest()
    return url, digest


def adapted_source(source: str) -> str:
    source = source.replace("require dirname(__DIR__) . $vendor;",
                            "require __DIR__ . '/vendor/autoload.php';")
    source = source.replace("require __DIR__ . $vendor;",
                            "require __DIR__ . '/vendor/autoload.php';")
    source = source.replace("/safe_svg/vendor/darylldoyle/safe-svg/includes/",
                            "/vendor/darylldoyle/safe-svg/includes/")
    return re.sub(r"(?m)^\s*require __DIR__ .*vendor/autoload\.php';",
                  "    require __DIR__ . '/vendor/autoload.php';", source)


def stage(format_name: str, package: str) -> Path:
    catalog = ROOT / "data/php" / format_name / "parsers.json"
    parser, = [item for item in json.loads(catalog.read_text()) if item["name"] == package]
    if "composer_lock" not in parser:
        raise ValueError("parser has no Composer source lock")
    original_lock = ROOT / parser["composer_lock"]
    augmented = augmented_lock(original_lock)
    composer_lock = json.loads((augmented / "composer.lock").read_text())
    release, = [item for item in composer_lock["packages"] if item["name"] == package]
    if release["version"] != parser["version"]:
        raise ValueError(f"Composer release differs from catalog: {package}")
    source_ref = release["source"]["reference"]
    source_url, digest = release_archive(release["dist"]["url"])
    control = ROOT / parser["control"]
    if not control.is_file():
        raise ValueError("no saved valid control")
    adapter = ROOT / parser["adapter"]
    source = adapter.read_text()
    uses_package_arg = bool(re.search(r"\$argv\s*\[\s*2\s*\]", source)
                            or re.search(r"\[\s*\$script\s*,\s*\$package\s*,", source))
    slug = re.sub(r"[^a-z0-9]+", "_", package.lower()).strip("_")
    destination = ROOT / "projects" / format_name / "php" / slug
    for existing in destination.parent.glob("*/manifest.json"):
        if json.loads(existing.read_text()).get("package") == package:
            raise ValueError(f"package already staged: {existing.parent}")
    if destination.exists():
        raise ValueError(f"project exists: {destination}")
    destination.mkdir(parents=True)
    shutil.copyfile(augmented / "composer.json", destination / "composer.json")
    shutil.copyfile(augmented / "composer.lock", destination / "composer.lock")
    adapted = adapted_source(source)
    if package == "uberchel/mediainfo4php":
        adapted = adapted.replace("        $parsed = \\uberchel\\MediaInfo::Get($path, false);",
                                  "        require_once __DIR__ . '/vendor/uberchel/mediainfo4php/mediainfo.php';\n"
                                  "        $parsed = \\uberchel\\MediaInfo::Get($path, false);")
    if package == "gufy/pdftohtml-php":
        adapted = adapted.replace("/opt/homebrew/bin/pdfinfo", "/usr/bin/pdfinfo")
        adapted = adapted.replace("/opt/homebrew/bin/pdftohtml", "/usr/bin/pdftohtml")
        adapted = adapted.replace("        $document = new \\Gufy\\PdfToHtml\\Pdf($path);",
                                  "        \\Gufy\\PdfToHtml\\Config::set('pdftohtml.output', '/tmp/parsarium-pdftohtml');\n"
                                  "        $document = new \\Gufy\\PdfToHtml\\Pdf($path);")
    (destination / "adapter.php").write_text(adapted)
    if package == "pyrex-fwi/id3":
        (destination / "pyrex").mkdir()
        shutil.copyfile(adapter.parent / "pyrex/mediainfo_oldxml.sh",
                        destination / "pyrex/mediainfo_oldxml.sh")
    args = f"['/work/adapter.php', {json.dumps(package)}, $path]" if uses_package_arg else "['/work/adapter.php', $path]"
    harness = f'''<?php
declare(strict_types=1);

function parsarium_parse(string $input): array {{
    if ($input === '' || strlen($input) > (1 << 20)) {{
        throw new InvalidArgumentException('input outside harness limit');
    }}
    $parsariumTemp = tempnam('/tmp', 'parsarium-{format_name}-');
    if ($parsariumTemp === false) {{ throw new RuntimeException('cannot create parser input'); }}
    $path = $parsariumTemp . '{control.suffix}';
    if (!rename($parsariumTemp, $path)) {{ throw new RuntimeException('cannot name parser input'); }}
    try {{
        if (file_put_contents($path, $input) !== strlen($input)) {{
            throw new RuntimeException('cannot write parser input');
        }}
        $argv = {args};
        $argc = count($argv);
        ob_start();
        try {{ require __DIR__ . '/adapter.php'; $text = (string) ob_get_clean(); }}
        catch (Throwable $error) {{ ob_end_clean(); throw $error; }}
        $lines = preg_split('/\\r?\\n/', trim($text));
        $last = end($lines);
        $observed = json_decode((string) $last, true, 512, JSON_THROW_ON_ERROR);
        if (!is_array($observed)) {{ throw new RuntimeException('adapter emitted no JSON object'); }}
        return $observed;
    }} finally {{ @unlink($path); }}
}}
'''
    harness = harness.replace("$path", "$parsariumInputPath")
    (destination / "harness.php").write_text(harness)
    run_control = '''<?php
declare(strict_types=1);
if (!function_exists('xdebug_start_code_coverage')) {
    throw new RuntimeException('Xdebug coverage extension is missing');
}
xdebug_start_code_coverage();
require __DIR__ . '/harness.php';
$data = file_get_contents('/input/control');
if ($data === false) { throw new RuntimeException('cannot read valid control'); }
$observed = parsarium_parse($data);
$expected = json_decode(EXPECTED_JSON, true, 512, JSON_THROW_ON_ERROR);
if ($observed != $expected) { throw new RuntimeException('control mismatch: ' . json_encode($observed)); }
$raw = xdebug_get_code_coverage();
$files = [];
$total = 0;
foreach ($raw as $filename => $lines) {
    if (!str_starts_with($filename, PACKAGE_PREFIX)) { continue; }
    $executed = [];
    foreach ($lines as $line => $hits) { if ($hits > 0) { $executed[] = (int) $line; } }
    sort($executed);
    $total += count($executed);
    $files[] = ['filename' => $filename,
                'summary' => ['lines' => ['covered' => count($executed)]],
                'executed_lines' => $executed];
}
if ($total === 0) { throw new RuntimeException('no PHP parser package source lines covered'); }
$coverage = ['data' => [['files' => $files]]];
$summary = ['control_pass' => true, 'output' => $observed,
            'parser_source_files' => count($files), 'parser_source_lines_covered' => $total,
            'coverage' => '/coverage/coverage.json'];
file_put_contents('/coverage/observed.json', json_encode($observed, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR) . "\\n");
file_put_contents('/coverage/coverage.json', json_encode($coverage, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR) . "\\n");
file_put_contents('/coverage/summary.json', json_encode($summary, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR) . "\\n");
echo json_encode($summary, JSON_THROW_ON_ERROR), "\\n";
'''
    run_control = run_control.replace("EXPECTED_JSON", json.dumps(json.dumps(parser["expected_output"])))
    run_control = run_control.replace("PACKAGE_PREFIX", json.dumps(f"/work/vendor/{package}/"))
    (destination / "run-control.php").write_text(run_control)
    (destination / "fuzz-target.php").write_text('''<?php
declare(strict_types=1);
/** @var PhpFuzzer\\Config $config */
require __DIR__ . '/harness.php';
$config->setTarget(static function (string $input): void { parsarium_parse($input); });
$config->setMaxLen(1 << 20);
''')
    runtime_extra = {
        "png": "libvips42t64 php8.5-imagick imagemagick",
        "ascii_pnm": "libvips42t64 php8.5-imagick imagemagick",
        "svg": "libvips42t64 php8.5-imagick imagemagick librsvg2-bin",
        "mp3_id3v2": "ffmpeg mediainfo",
        "wav": "ffmpeg mediainfo",
        "mp4": "ffmpeg mediainfo",
        "pdf": "poppler-utils php8.5-imagick php8.5-curl imagemagick",
    }.get(format_name, "")
    if package == "maximal/audio-waveform":
        runtime_extra += " sox"
    runtime_env = ("ENV PARSARIUM_RSVG_CONVERT=/usr/bin/rsvg-convert\n"
                   if format_name == "svg" else "")
    extra_runtime_files = ("COPY pyrex/mediainfo_oldxml.sh /work/pyrex/mediainfo_oldxml.sh\n"
                           "RUN chmod +x /work/pyrex/mediainfo_oldxml.sh\n"
                           if package == "pyrex-fwi/id3" else "")
    docker = f'''FROM --platform=linux/arm64 {BASE_IMAGE} AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \\
    ca-certificates composer curl php8.5-cli php8.5-mbstring php8.5-gd php8.5-zip php8.5-xml unzip \\
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-plugins --no-interaction --no-progress --prefer-dist --ignore-platform-reqs \\
    && curl --fail --location --retry 3 {source_url} --output /work/parser-source.zip \\
    && echo '{digest}  /work/parser-source.zip' | sha256sum --check
RUN {{ php --version | head -1; composer --version; }} > /work/toolchain.txt

FROM --platform=linux/arm64 {BASE_IMAGE}
ENV DEBIAN_FRONTEND=noninteractive
{runtime_env}RUN apt-get update -qq && apt-get install -y --no-install-recommends \\
    php8.5-cli php8.5-mbstring php8.5-gd php8.5-zip php8.5-xml php8.5-xdebug {runtime_extra} \\
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/vendor /work/vendor
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.php harness.php fuzz-target.php run-control.php /work/
{extra_runtime_files}ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/run-control.php"]
'''
    (destination / "Dockerfile").write_text(docker)
    (destination / "source-lock.json").write_text(json.dumps({package: {
        "release": parser["version"], "source_sha256": digest,
        "composer_reference": source_ref, "archive_url": source_url}}, indent=2) + "\n")
    manifest = json.loads((TEMPLATE / "manifest.json").read_text())
    manifest.pop("format_specific_coverage_file_suffix", None)
    manifest.update({"format": format_name, "package": package, "release": parser["version"],
                     "catalog_parser": str(catalog.relative_to(ROOT)),
                     "source_lock": str((destination / "source-lock.json").relative_to(ROOT)),
                     "source_sha256": digest, "control": parser["control"],
                     "control_sha256": sha256(control.read_bytes()).hexdigest(),
                     "expected_output": parser["expected_output"],
                     "coverage_subject_prefix": f"/work/vendor/{package}/",
                     "coverage": f"Xdebug executed line coverage in {package} PHP source; php-fuzzer basic-block instrumentation for fuzz entry"})
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return destination


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("format")
    cli.add_argument("package")
    args = cli.parse_args()
    print(stage(args.format, args.package).relative_to(ROOT))
