package main

import (
	"bytes"

	"encoding/json"
	"fmt"

	"os"

	dedalo "github.com/pydpll/dedalo/obj"
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

	case "github.com/pydpll/dedalo/obj":
		mesh, err := dedalo.ParsePLY(bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		output = map[string]any{"vertices": mesh.NumVertices(), "faces": mesh.NumFaces()}

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
