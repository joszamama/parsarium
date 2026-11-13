package main

import (
	"encoding/json"
	"os"

	"github.com/cpmech/gosl/la"
)

func main() {
	if len(os.Args) != 2 {
		panic("expected one local Matrix Market path")
	}
	var matrix la.Triplet
	symmetric := matrix.ReadSmat(os.Args[1], true)
	rows, cols := matrix.Size()
	dense := matrix.ToDense()
	output := map[string]any{
		"rows": rows, "cols": cols, "entries": matrix.Len(),
		"value_0_2": dense.Get(0, 2), "symmetric": symmetric,
	}
	if err := json.NewEncoder(os.Stdout).Encode(output); err != nil {
		panic(err)
	}
}
