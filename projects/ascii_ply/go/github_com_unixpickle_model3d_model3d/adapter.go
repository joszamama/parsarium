package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/unixpickle/model3d/model3d"
)

// The documented model3d.ReadColorPLY(io.Reader) reads the PLY through the
// model3d fileformats PLYReader and returns the triangle faces and a
// per-vertex colour map.
func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL")
	}
	name, path := os.Args[1], os.Args[2]
	output := map[string]any{}
	switch name {

	case "github.com/unixpickle/model3d/model3d":
		file, err := os.Open(path)
		if err != nil {
			panic(err)
		}
		defer file.Close()
		triangles, colors, err := model3d.ReadColorPLY(file)
		if err != nil {
			fmt.Println(`{"error":"rejected"}`)
			return
		}
		first := [][]float64{}
		if len(triangles) > 0 {
			for _, c := range triangles[0] {
				first = append(first, []float64{c.X, c.Y, c.Z})
			}
		}
		output = map[string]any{"triangles": len(triangles), "first_triangle": first,
			"coloured_vertices": colors.Len()}

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
