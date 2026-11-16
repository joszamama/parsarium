"""Stage the tagged SPly fork from the verified RPly callback harnesses."""

from hashlib import sha256
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = json.loads((ROOT / "data/c/ascii_ply/source-lock.json").read_text())["sply"]
OLD_URL = "https://w3.impa.br/~diego/software/rply/rply-1.1.4.tar.gz"


for ecosystem in ("c",):
    catalog = ROOT / "data" / ecosystem / "ascii_ply/parsers.json"
    parser, = (item for item in json.loads(catalog.read_text()) if item["name"] == "sply")
    source = ROOT / "projects/ascii_ply" / ecosystem / "rply"
    target = source.with_name("sply")
    if target.exists():
        raise SystemExit(f"project already exists: {target}")
    target.mkdir()
    for file in source.iterdir():
        if file.is_dir() or file.name in {"README.md", "verification.json"}:
            continue
        text = file.read_text()
        if file.name == "Dockerfile":
            text = text.replace(OLD_URL, SOURCE["source_url"])
        text = (text.replace("rply", "sply")
                    .replace("RPly", "SPly")
                    .replace("1.1.4", SOURCE["release"])
                    .replace("daf0b060fe701adf72aab0d525323d2e2e1bde9aa6aa9713ff1a5ef1e768d703",
                             SOURCE["source_sha256"]))
        (target / file.name).write_text(text)
    lock = {"sply": {"release": SOURCE["release"],
                     "source_sha256": SOURCE["source_sha256"]}}
    (target / "source-lock.json").write_text(json.dumps(lock, indent=2) + "\n")
    manifest = json.loads((target / "manifest.json").read_text())
    manifest["package"] = "sply"
    manifest["release"] = SOURCE["release"]
    manifest["source_sha256"] = SOURCE["source_sha256"]
    manifest["expected_output"] = parser["expected_output"]
    manifest["source_lock"] = str((target / "source-lock.json").relative_to(ROOT))
    manifest["catalog_parser"] = str(catalog.relative_to(ROOT))
    manifest["control"] = parser["control"]
    manifest["control_sha256"] = sha256((ROOT / parser["control"]).read_bytes()).hexdigest()
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(target.relative_to(ROOT))
