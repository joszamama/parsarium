#!/usr/bin/env python3
"""Consistency checks for data/expansion (JSON/XML/plain-MP3 inventory). Exit 1 on any failure."""
import hashlib, json, sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "data/expansion"
FORMATS = ["json", "xml", "mp3_plain"]
ECOS = ["c", "cpp", "go", "java", "javascript", "python", "rust", "php"]
STD_OK = {"standard_api_verified", "runtime_api_verified", "none_documented_in_scoped_standard_library",
          "none_documented_in_scoped_runtime_apis", "none_verified_negative_probe", "runtime_api_documented_pending_control"}
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


def mpeg_frames(b):
    """Walk contiguous MPEG-1/2 Layer III frames; return (frames, version) or raise."""
    br = {3: [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320], 2: [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160]}
    sr = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000]}
    i = n = 0
    vers = set()
    while i < len(b):
        h = b[i:i + 4]
        assert len(h) == 4 and h[0] == 0xFF and (h[1] & 0xE0) == 0xE0, f"no sync at {i}"
        v, layer = (h[1] >> 3) & 3, (h[1] >> 1) & 3
        assert v in (2, 3) and layer == 1, f"not MPEG-1/2 Layer III at {i}"
        rate, bitrate = sr[v][(h[2] >> 2) & 3], br[v][h[2] >> 4] * 1000
        side = (17 if (h[3] >> 6) == 3 else 32) if v == 3 else (9 if (h[3] >> 6) == 3 else 17)
        tag = b[i + 4 + (0 if h[1] & 1 else 2) + side:][:4]
        assert tag not in (b"Xing", b"Info", b"VBRI"), f"Xing/Info/VBRI frame at {i}"
        i += (144 if v == 3 else 72) * bitrate // rate + ((h[2] >> 1) & 1)
        n += 1
        vers.add(v)
    assert i == len(b), "trailing bytes after last frame"
    return n, vers


formats = json.loads((EXP / "formats.json").read_text())
receipts = json.loads((EXP / "standard-receipts.json").read_text())["receipts"]

# Controls
for name, sha in formats["control_sha256"].items():
    p = EXP / "controls" / name
    check(p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() == sha, f"control hash mismatch: {name}")
j = json.loads((EXP / "controls/control.json").read_bytes())
check(j["nested"]["text"] == "café ✓" and len(j["items"]) == 6, "JSON control content")
r = ET.fromstring((EXP / "controls/control.xml").read_bytes())
check(r.tag == "{urn:parsarium:control}catalog" and len(r) == 3, "XML control content")
for name in formats["formats"]["mp3_plain"]["controls"]:
    b = (EXP / "controls" / name).read_bytes()
    check(not b.startswith(b"ID3") and b[-128:-125] != b"TAG" and b"APETAGEX" not in b, f"{name}: tag present")
    try:
        n, vers = mpeg_frames(b)
        check(n == formats["control_expected"][name]["frames"], f"{name}: {n} frames, expected {formats['control_expected'][name]['frames']}")
    except AssertionError as e:
        errors.append(f"{name}: {e}")

# Receipts
for rc in receipts:
    p = ROOT / rc["control"]
    check(hashlib.sha256(p.read_bytes()).hexdigest() == rc["control_sha256"], f"receipt control hash stale: {rc['api']} {rc['control']}")
    check(rc["passed"] is True, f"receipt failed: {rc['ecosystem']} {rc['api']} {rc['control']}")

# Cells
inv = json.loads((EXP / "inventory.json").read_text())
check(inv["selected_third_party_total"] == 0, "inventory selected total must be 0")
check(len(inv["cells"]) == len(FORMATS) * len(ECOS), "inventory cell count")
for fmt in FORMATS:
    for eco in ECOS:
        p = EXP / "cells" / fmt / f"{eco}.json"
        if not p.exists():
            errors.append(f"missing {p}")
            continue
        c = json.loads(p.read_text())
        tag = f"{fmt}/{eco}"
        check(c["selected_third_party"] == [] and c["selected_count"] == 0, f"{tag}: selection must be empty (no verified packages)")
        check(c["search"]["queries"] and all(q.get("error") is None for q in c["search"]["queries"]), f"{tag}: search missing or errored")
        check(all(q["hits_recorded"] <= c["search"]["limit_per_query"] for q in c["search"]["queries"]), f"{tag}: hits exceed limit")
        met = json.loads((EXP / "metrics" / f"{eco}.json").read_text())
        check(c["metric"]["name"] == met["metric"], f"{tag}: metric not the ecosystem metric")
        order = []
        for l in c["leads"]:
            check(l["verified"] is False, f"{tag}: {l['name']} marked verified")
            check(l["status"] in ("lead", "excluded_scope"), f"{tag}: {l['name']} bad status")
            check(l["source"] is None or l["source"].startswith("https://"), f"{tag}: {l['name']} source not https")
            check(l["source"] is not None or l["found_by"] == "targeted_documentation_lead", f"{tag}: {l['name']} no source")
            check(l["metric_value"] is not None or l["metric_error"], f"{tag}: {l['name']} null metric without reason")
            check(l["metric_value"] is None or (isinstance(l["metric_value"], int) and l["metric_value"] >= 0), f"{tag}: {l['name']} bad metric")
            check("lead_adoption_order" not in l or l["status"] == "lead", f"{tag}: excluded lead ranked")
            if fmt == "mp3_plain" and "tags only" in (l["note"] or "").lower().replace("-", " "):
                check(l["status"] == "excluded_scope", f"{tag}: tag-only lead {l['name']} not excluded")
            if "lead_adoption_order" in l:
                order.append((l["lead_adoption_order"], l["metric_value"]))
        order.sort()
        check([o for o, _ in order] == list(range(1, len(order) + 1)), f"{tag}: adoption order not contiguous")
        check(all(order[i][1] >= order[i + 1][1] for i in range(len(order) - 1)), f"{tag}: adoption order not descending")
        s = c["standard_or_runtime"]
        check(s["status"] in STD_OK, f"{tag}: bad standard status {s['status']}")
        check(s["counts_toward_ten"] is False and s["official_documentation"], f"{tag}: standard docs/ceiling")
        if s["status"].endswith("_verified"):
            check(any(r["passed"] and r["kind"] == "positive" for r in s["receipts"]), f"{tag}: verified without positive receipt")
        if s["status"] == "none_verified_negative_probe":
            check(any(r["kind"] == "negative_probe" for r in s["receipts"]), f"{tag}: negative status without probe")

# No leakage into the selected catalog
cells = json.loads((ROOT / "data/cells.json").read_text())["cells"]
check(not any(c["format"] in FORMATS for c in cells), "expansion format leaked into data/cells.json")
for fmt in FORMATS:
    check(not (ROOT / "catalog" / fmt).exists(), f"catalog/{fmt} must not exist")
check(not (ROOT / "data/curation/preten/c/json").exists(), "expansion leaked into curation")

if errors:
    print("FAIL", len(errors))
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(FORMATS) * len(ECOS)} cells, {sum(len(json.loads((EXP / 'cells' / f / f'{e}.json').read_text())['leads']) for f in FORMATS for e in ECOS)} lead entries, "
      f"{len(receipts)} standard receipts, 0 selected third-party paths")
