#!/usr/bin/env python3
"""Run the standard/runtime API controls for the expansion inventory and write receipts.

Third-party packages are not run here. Writes data/expansion/standard-receipts.json.
"""
import datetime, hashlib, json, platform, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "data/expansion"
A = EXP / "adapters"
C = EXP / "controls"

JSON_EXPECTED = {"count": 3, "items": 6, "keys": ["count", "format", "items", "nested"], "text": "café ✓"}
XML_EXPECTED = {"children": 3, "ids": ["a", "b"], "root": "{urn:parsarium:control}catalog", "texts": ["café", "x<y"]}
MP3_REJECT = {"accepted": False, "exception": "UnsupportedAudioFileException"}

RUNS = [
    # (ecosystem, format, api, cmd prefix, cwd, control, expected, kind)
    ("python", "json", "json.loads", ["python3", "-I", str(A / "python/std.py")], None, "control.json", JSON_EXPECTED, "positive"),
    *[("python", "xml", api, ["python3", "-I", str(A / "python/std.py")], None, "control.xml", XML_EXPECTED, "positive")
      for api in ("xml.etree.ElementTree.fromstring", "xml.dom.minidom.parseString", "xml.parsers.expat.ParserCreate")],
    ("go", "json", "encoding/json.Unmarshal", ["go", "run", "."], A / "go", "control.json", JSON_EXPECTED, "positive"),
    ("go", "xml", "encoding/xml.Decoder.Token", ["go", "run", "."], A / "go", "control.xml", XML_EXPECTED, "positive"),
    ("php", "json", "json_decode", ["php", str(A / "php/std.php")], None, "control.json", JSON_EXPECTED, "positive"),
    *[("php", "xml", api, ["php", str(A / "php/std.php")], None, "control.xml", XML_EXPECTED, "positive")
      for api in ("simplexml_load_string", "DOMDocument::loadXML", "XMLReader::XML")],
    *[("java", "xml", api, ["java", str(A / "java/StdControl.java")], None, "control.xml", XML_EXPECTED, "positive")
      for api in ("javax.xml.parsers.DocumentBuilder.parse", "javax.xml.stream.XMLStreamReader")],
    *[("java", "mp3_plain", "javax.sound.sampled.AudioSystem.getAudioFileFormat", ["java", str(A / "java/StdControl.java")], None, m, MP3_REJECT, "negative_probe")
      for m in ("silent-plain-44k.mp3", "tone-plain-16k.mp3")],
]


def version(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return (r.stdout + r.stderr).strip().splitlines()[0]
    except Exception as e:
        return f"unavailable: {e!r}"


def main():
    runtimes = {"python": version(["python3", "-V"]), "go": version(["go", "version"]), "php": version(["php", "-v"]),
                "java": version(["java", "-version"]), "javascript": version(["node", "-v"])}
    receipts = []
    for eco, fmt, api, cmd, cwd, control, expected, kind in RUNS:
        path = C / control
        full = [*cmd, api, str(path.resolve())]
        r = subprocess.run(full, capture_output=True, text=True, cwd=cwd, timeout=300)
        try:
            observed = json.loads(r.stdout)
        except ValueError:
            observed = None
        receipts.append({"ecosystem": eco, "format": fmt, "api": api, "kind": kind, "runtime": runtimes[eco],
                         "adapter": str(Path(cmd[-1] if cwd is None else cwd).relative_to(ROOT)),
                         "control": str(path.relative_to(ROOT)), "control_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                         "exit_code": r.returncode, "observed": observed, "expected": expected,
                         "passed": r.returncode == 0 and observed == expected, "stderr_tail": r.stderr[-400:] or None})
        print(eco, fmt, api, receipts[-1]["passed"])
    out = {"captured_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "host": f"{platform.system()} {platform.release()} {platform.machine()}", "runtimes": runtimes,
           "scope": "Standard/runtime APIs only. Not counted toward any ten-path ceiling. Third-party leads were not run.",
           "receipts": receipts}
    (EXP / "standard-receipts.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
