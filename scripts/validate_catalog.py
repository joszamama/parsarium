"""Check cross-file consistency of accepted cells and their recorded evidence."""

from pathlib import Path
import json


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
        assert len({hit["name"] for search in snapshot["search"] for hit in search["hits"]}) == cell["unique_search_hits"]
        assert len(snapshot["search"]) == len(cell["search_queries"])
        leads = read(f"{key}/leads.json")
        assert sum(lead["status"] == "unresolved" for lead in leads) == cell["unresolved_documentation_leads"]
        assert not ({lead["name"] for lead in leads} & {p["name"] for p in parsers})
        for parser in parsers:
            name = parser["name"]
            assert parser["version"] == lock[name]
            assert parser["version"] == snapshot["releases"][name]["version"]
            assert isinstance(snapshot["download_metric"]["packages"][name]["downloads"], int)
            assert parser["license"] and parser["documentation"] and parser["family"] and parser["input_api"]
        results = read(f"{key}/verification.json")
        runs = results["results"] if cell["format"] == "png" else results["third_party"]
        assert {r["package"] for r in runs} == {p["name"] for p in parsers}
        assert all(r["pass"] for r in runs)
        if cell["format"] == "png":
            assert read(f"{key}/browser-verification.json")["pass"]
        elif cell["verified_standard_or_runtime_count"]:
            assert results["runtime"]["pass"]
        assert cell["verified_standard_or_runtime_count"] == len(read(f"{key}/standard.json")["verified_apis"])
    print(f"Validated {len(matrix)} cells, {sum(c['status'] != 'not_started' for c in matrix)} with recorded evidence")


if __name__ == "__main__":
    main()
