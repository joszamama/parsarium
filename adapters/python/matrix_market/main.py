"""Parse a local Matrix Market control with one pinned Python package."""

import json
import sys
from pathlib import Path


def dense_result(matrix):
    return {"shape": list(matrix.shape), "values": matrix.tolist()}


def parse(name, path):
    path = Path(path)
    if name == "scipy":
        from scipy.io import mmread
        return dense_result(mmread(str(path), spmatrix=False).toarray())

    if name == "fast-matrix-market":
        import fast_matrix_market as fmm
        return dense_result(fmm.mmread(str(path)).toarray())

    if name == "anndata":
        from anndata.io import read_mtx
        return dense_result(read_mtx(str(path)).X.toarray())

    if name == "scanpy":
        import scanpy
        return dense_result(scanpy.read_mtx(str(path)).X.toarray())

    if name == "python-graphblas":
        import graphblas as gb
        return dense_result(gb.io.mmread(str(path)).to_dense(fill_value=0))

    if name == "gensim":
        from gensim.corpora import MmCorpus
        corpus = MmCorpus(str(path))
        return {"shape": [corpus.num_docs, corpus.num_terms],
                "entries": [[list(item) for item in document] for document in corpus]}

    if name == "rustworkx":
        import rustworkx as rx
        graph = rx.read_matrix_market_file(str(path))
        return {"vertices": len(graph),
                "edges": sorted([u, v] for u, v, _ in graph.weighted_edge_list())}

    if name == "subgraphsearch":
        import subgraphsearch as ss
        graph = ss.read(str(path))
        return {"vertices": graph.n,
                "edges": sorted(graph.edges().tolist())}

    if name == "muon":
        import muon
        data = muon.read_10x_mtx(str(path))
        return {"shape": list(data.mod["rna"].shape),
                "values": data.mod["rna"].X.toarray().tolist(),
                "cells": list(data.mod["rna"].obs_names),
                "genes": list(data.mod["rna"].var_names)}

    if name == "crest-sc":
        import crest
        data = crest.read_10x_mtx(str(path))
        return {"shape": list(data.shape),
                "values": data.to_scipy().toarray().tolist(),
                "cells": data.obs["barcode"].to_list(),
                "genes": data.var["gene_name"].to_list()}

    if name == "scprep":
        import scprep
        matrix = scprep.io.load_mtx(str(path), sparse=False)
        return dense_result(matrix)

    if name == "acidgenomics-pipette":
        import pipette
        return dense_result(pipette.read(str(path)).toarray())

    raise ValueError(f"unknown parser: {name}")


if __name__ == "__main__":
    print(json.dumps(parse(sys.argv[1], sys.argv[2]), sort_keys=True))
