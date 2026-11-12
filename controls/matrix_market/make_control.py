"""Generate small valid NIST Matrix Market coordinate controls."""

from pathlib import Path
import gzip


HERE = Path(__file__).resolve().parent
CONTROLS = {
    "real-general.mtx": (
        "%%MatrixMarket matrix coordinate real general\n"
        "% Parsarium: 2-by-3 sparse real matrix\n"
        "2 3 3\n"
        "1 1 1.5\n"
        "1 3 -2\n"
        "2 2 4\n"
    ),
    "graph-general.mtx": (
        "%%MatrixMarket matrix coordinate real general\n"
        "% Parsarium: three vertices and two graph edges\n"
        "3 3 2\n"
        "1 2 7.0\n"
        "2 3 5.0\n"
    ),
    "graph-no-comment.mtx": (
        "%%MatrixMarket matrix coordinate real general\n"
        "3 3 2\n"
        "1 2 7.0\n"
        "2 3 5.0\n"
    ),
    "real-symmetric.mtx": (
        "%%MatrixMarket matrix coordinate real symmetric\n"
        "% Parsarium: three diagonal entries in a symmetric matrix\n"
        "3 3 3\n"
        "1 1 1\n"
        "2 2 2\n"
        "3 3 3\n"
    ),
}


for name, content in CONTROLS.items():
    path = HERE / name
    path.write_bytes(content.encode("ascii"))
    print(f"Wrote {name}: {path.stat().st_size} bytes")

tenx = HERE / "tenx_v3"
tenx.mkdir(exist_ok=True)
tenx_files = {
    "matrix.mtx.gz": (
        "%%MatrixMarket matrix coordinate integer general\n"
        "% Parsarium: two genes by three cells\n"
        "2 3 3\n"
        "1 1 2\n"
        "1 3 4\n"
        "2 2 5\n"
    ),
    "features.tsv.gz": "GENE-1\tGeneA\tGene Expression\nGENE-2\tGeneB\tGene Expression\n",
    "barcodes.tsv.gz": "CELL-A\nCELL-B\nCELL-C\n",
}
for name, content in tenx_files.items():
    path = tenx / name
    path.write_bytes(gzip.compress(content.encode("ascii"), mtime=0))
    print(f"Wrote {path.relative_to(HERE)}: {path.stat().st_size} bytes")
