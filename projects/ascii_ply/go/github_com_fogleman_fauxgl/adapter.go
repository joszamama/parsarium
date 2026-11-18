package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/fogleman/fauxgl"
)

// The documented fauxgl.LoadPLY(path) parses the PLY header and, for the
// ASCII encoding, the vertex and face rows into a triangle mesh.
func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL")
	}
	name, path := os.Args[1], os.Args[2]
	output := map[string]any{}
	switch name {

	case "github.com/fogleman/fauxgl":
		mesh, err := fauxgl.LoadPLY(path)
		if err != nil {
			fmt.Println(`{"error":"rejected"}`)
			return
		}
		first := [][]float64{}
		if len(mesh.Triangles) > 0 {
			t := mesh.Triangles[0]
			for _, v := range []fauxgl.Vector{t.V1.Position, t.V2.Position, t.V3.Position} {
				first = append(first, []float64{v.X, v.Y, v.Z})
			}
		}
		output = map[string]any{"triangles": len(mesh.Triangles), "first_triangle": first}

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
