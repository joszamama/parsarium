package main

import (
	"bytes"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	"github.com/HerrMotz/Algorithmic-Network-Analysis-Library/graphlib"
	tensor "github.com/fumin/tensor"
	gosparse "github.com/go-sparse/sparse/mtx"
	market "github.com/wamuir/matrix-market"
	utils "gitlab.com/Grouumf/ATACdemultiplex/ATACdemultiplexUtils"
	grouumf "gitlab.com/Grouumf/enhlinktools/matrix"
	"route-planning/graphio"
	"suitesparse-dl/conv"
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
	case "github.com/fumin/tensor":
		matrix, err := tensor.ReadMatrixMarket(bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		shape := matrix.Shape()
		output = map[string]any{"rows": shape[0], "cols": shape[1], "value_0_2": real(matrix.At(0, 2))}
	case "github.com/senniraf/route-planning/graphio":
		edges, vertices, err := graphio.NewMTXInput(path).LoadGraph()
		if err != nil {
			panic(err)
		}
		edge01 := false
		for _, edge := range edges {
			if edge.From == 0 && edge.To == 1 {
				edge01 = true
			}
		}
		output = map[string]any{"vertices": vertices, "edges": len(edges), "edge_0_1": edge01}
	case "github.com/hpcde/spmv-acc/tools/suitesparse-dl/conv":
		output = convertMatrixMarket(path)
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

func convertMatrixMarket(path string) map[string]any {
	file, err := os.CreateTemp("", "parsarium-mtx-*.bin")
	if err != nil {
		panic(err)
	}
	outputPath := file.Name()
	file.Close()
	defer os.Remove(outputPath)
	if err := conv.ConvertOneMtx(path, outputPath, true); err != nil {
		panic(err)
	}
	converted, err := os.Open(outputPath)
	if err != nil {
		panic(err)
	}
	defer converted.Close()
	var magic, version, valueType, rows, cols, entries int32
	for _, field := range []*int32{&magic, &version, &valueType, &rows, &cols, &entries} {
		if err := binary.Read(converted, binary.LittleEndian, field); err != nil {
			panic(err)
		}
	}
	if magic != 0x20211015 || version != 2 || valueType != 3 {
		panic("unexpected converted matrix header")
	}
	rowPointers := make([]int32, rows+1)
	columnIndices := make([]int32, entries)
	values := make([]float64, entries)
	for _, field := range []any{rowPointers, columnIndices, values} {
		if err := binary.Read(converted, binary.LittleEndian, field); err != nil {
			panic(err)
		}
	}
	var value02 float64
	found := false
	for i := rowPointers[0]; i < rowPointers[1]; i++ {
		if columnIndices[i] == 2 {
			value02, found = values[i], true
		}
	}
	if !found {
		panic("expected control entry absent from converted matrix")
	}
	return map[string]any{"rows": rows, "cols": cols, "entries": entries, "value_0_2": value02}
}
