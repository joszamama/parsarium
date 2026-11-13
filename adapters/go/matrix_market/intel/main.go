package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/intel/forGraphBLASGo/GrB"
	"github.com/intel/forLAGraphGo/LAGraph"
	"github.com/intel/forLAGraphGo/LAGraph/MatrixMarket"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	if len(os.Args) != 2 {
		panic("expected one local Matrix Market path")
	}
	must(LAGraph.Init(GrB.Blocking))
	defer func() { must(LAGraph.Finalize()) }()

	file, err := os.Open(os.Args[1])
	must(err)
	defer file.Close()
	matrix, err := MatrixMarket.Read[float64](file)
	must(err)
	defer func() { must(matrix.Free()) }()

	rows, err := matrix.Nrows()
	must(err)
	cols, err := matrix.Ncols()
	must(err)
	entries, err := matrix.Nvals()
	must(err)
	value, present, err := matrix.ExtractElement(0, 2)
	must(err)
	if !present {
		panic("the control entry at (1,3) was absent")
	}
	output := struct {
		Rows    int     `json:"rows"`
		Cols    int     `json:"cols"`
		Entries int     `json:"entries"`
		Value   float64 `json:"value_0_2"`
	}{rows, cols, entries, value}
	encoded, err := json.Marshal(output)
	must(err)
	fmt.Println(string(encoded))
}
