"""Check cross-file consistency of accepted cells and their recorded evidence."""

from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]


def read(path: str):
    return json.loads((ROOT / path).read_text())


def main() -> None:
    matrix = read("data/cells.json")["cells"]
    assert len(matrix) == 88
    assert len({(c["ecosystem"], c["format"]) for c in matrix}) == 88
    lock = read("package-lock.json")["packages"][""]["dependencies"]
    for cell in matrix:
        assert cell["working_target"] == 20 and cell["ceiling"] == 30
        if cell["status"] == "not_started":
            assert cell["verified_third_party_count"] == 0
            assert cell["search_hits_recorded"] == 0
            continue
        key = f"data/{cell['ecosystem']}/{cell['format']}"
        parsers = read(f"{key}/parsers.json")
        snapshot = read(f"{key}/registry-snapshot.json")
        assert len(parsers) == cell["verified_third_party_count"]
        assert len(parsers) <= cell["ceiling"]
        assert len({p["name"] for p in parsers}) == len(parsers)
        assert sum(len(s["hits"]) for s in snapshot["search"]) == cell["search_hits_recorded"]
        assert snapshot["search_limit_per_query"] == cell["search_limit_per_query"]
        hit_key = "packagePath" if cell["ecosystem"] == "go" else "name"
        assert len({hit[hit_key] for search in snapshot["search"] for hit in search["hits"]}) == cell["unique_search_hits"]
        assert len(snapshot["search"]) == len(cell["search_queries"])
        leads = read(f"{key}/leads.json")
        assert sum(lead["status"] == "unresolved" for lead in leads) == cell["unresolved_documentation_leads"]
        assert not ({lead["name"] for lead in leads} & {p["name"] for p in parsers})
        for parser in parsers:
            name = parser["name"]
            if cell["ecosystem"] == "go":
                go_mod = (ROOT / "adapters" / "go" / cell["format"] / "go.mod").read_text()
                go_versions = dict(re.findall(r"^\s*(\S+)\s+(v\S+)", go_mod, re.MULTILINE))
                assert parser["version"] == go_versions[parser["module"]]
                count = snapshot["popularity_metric"]["packages"][name]["imported_by_packages"]
                assert count is None or isinstance(count, int)
                assert parser["license"] == snapshot["releases"][name]["license"]
            elif cell["ecosystem"] == "python":
                requirements = (ROOT / "adapters" / "python" / cell["format"] / "requirements.in").read_text()
                python_versions = dict(re.findall(r"^([A-Za-z0-9_.-]+)==([^\s]+)$", requirements, re.MULTILINE))
                assert parser["version"] == python_versions[name]
                count = snapshot["download_metric"]["packages"][name]["downloads"]
                assert count is None or isinstance(count, int)
                assert (ROOT / parser["control"]).exists()
            else:
                assert parser["version"] == lock[name]
                assert isinstance(snapshot["download_metric"]["packages"][name]["downloads"], int)
            assert parser["version"] == snapshot["releases"][name]["version"]
            assert parser["license"] and parser["documentation"] and parser["family"] and parser["input_api"]
        results = read(f"{key}/verification.json")
        browser_png = cell["ecosystem"] == "javascript" and cell["format"] == "png"
        runs = results["results"] if browser_png else results["third_party"]
        assert {r["package"] for r in runs} == {p["name"] for p in parsers}
        assert all(r["pass"] for r in runs)
        if browser_png:
            assert read(f"{key}/browser-verification.json")["pass"]
        elif cell["verified_standard_or_runtime_count"]:
            runtime_results = results["runtime"]
            if isinstance(runtime_results, list):
                assert len(runtime_results) == cell["verified_standard_or_runtime_count"]
                assert all(row["pass"] for row in runtime_results)
            else:
                assert runtime_results["pass"]
        assert cell["verified_standard_or_runtime_count"] == len(read(f"{key}/standard.json")["verified_apis"])
    print(f"Validated {len(matrix)} cells, {sum(c['status'] != 'not_started' for c in matrix)} with recorded evidence")


if __name__ == "__main__":
    main()
