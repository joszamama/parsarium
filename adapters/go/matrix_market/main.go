package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	"github.com/HerrMotz/Algorithmic-Network-Analysis-Library/graphlib"
	gosparse "github.com/go-sparse/sparse/mtx"
	market "github.com/wamuir/matrix-market"
	utils "gitlab.com/Grouumf/ATACdemultiplex/ATACdemultiplexUtils"
	grouumf "gitlab.com/Grouumf/enhlinktools/matrix"
)

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL")
	}
	name, path := os.Args[1], os.Args[2]
	data, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	output := map[string]any{}
	switch name {
	case "github.com/go-sparse/sparse/mtx":
		matrix, err := gosparse.Read(bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		output = map[string]any{"rows": matrix.Rows, "cols": matrix.Cols, "entries": matrix.Entries, "value_0_2": matrix.Real.ToCSR().At(0, 2)}
	case "github.com/wamuir/matrix-market":
		var matrix market.COO
		_, err := matrix.UnmarshalTextFrom(bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		rows, cols := matrix.ToCOO().Dims()
		output = map[string]any{"rows": rows, "cols": cols, "value_0_2": matrix.ToCOO().At(0, 2)}
	case "github.com/HerrMotz/Algorithmic-Network-Analysis-Library/graphlib":
		graph, err := graphlib.ReadGraphAdjListAs(path, graphlib.FormatMatrixMarket, true)
		if err != nil {
			panic(err)
		}
		output = map[string]any{"vertices": graph.Size, "edges_from_0": len(graph.List[0])}
	case "gitlab.com/Grouumf/enhlinktools/matrix":
		controlDir := filepath.Dir(path)
		var matrix grouumf.SparseFloatMatrix
		matrix.Init(grouumf.Attributes{
			Xgi:     utils.Filename(filepath.Join(controlDir, "go-cols.tsv")),
			Ygi:     utils.Filename(filepath.Join(controlDir, "go-rows.tsv")),
			MatFile: utils.Filename(path), MatrixFormat: "cellRanger", NbThreads: 1,
		})
		matrix.LoadMatrix(nil, nil)
		output = map[string]any{"value_0_0": matrix.MatCol.GetRow(0)[0], "value_0_2": matrix.MatCol.GetRow(0)[2], "value_1_1": matrix.MatCol.GetRow(1)[1]}
	default:
		panic(fmt.Sprintf("unknown Matrix Market package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
