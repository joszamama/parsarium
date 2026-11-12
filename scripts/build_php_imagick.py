"""Build pinned PECL Imagick into ignored cache for PHP parser adapters."""

from hashlib import sha256
from pathlib import Path
import json
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / "data/php/ascii_pnm/pecl-imagick-lock.json").read_text())
CACHE = ROOT / "cache/pecl-imagick"
ARCHIVE = CACHE / "imagick-3.8.1.tgz"
SOURCE = CACHE / "imagick-3.8.1"
EXTENSION = SOURCE / "modules/imagick.so"


def build() -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    if not ARCHIVE.exists():
        subprocess.run(["curl", "-fsSL", "--max-time", "60", "--retry", "2",
                        LOCK["source_url"], "-o", str(ARCHIVE)], check=True)
    assert sha256(ARCHIVE.read_bytes()).hexdigest() == LOCK["source_sha256"]
    if not SOURCE.exists():
        subprocess.run(["tar", "-xzf", str(ARCHIVE), "-C", str(CACHE)], check=True)
    if not EXTENSION.exists():
        phpize = shutil.which("phpize")
        php_config = shutil.which("php-config")
        if phpize is None or php_config is None:
            raise RuntimeError("phpize and php-config are required")
        for command in ([phpize], ["./configure", f"--with-php-config={php_config}",
                                    "--with-imagick=/opt/homebrew"], ["make", "-j4"]):
            subprocess.run(command, cwd=SOURCE, check=True, capture_output=True, text=True)
    version = subprocess.run(["php", "-d", f"extension={EXTENSION}", "-r",
                              "echo phpversion('imagick');"], check=True, capture_output=True,
                             text=True).stdout.strip()
    assert version == LOCK["release"]
    return EXTENSION


if __name__ == "__main__":
    print(build())
