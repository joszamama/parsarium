package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/unixpickle/model3d/model3d"
)

// run reads the PLY with the documented model3d.ReadColorPLY(io.Reader), which
// uses the model3d fileformats PLYReader and returns the triangle faces and a
// per-vertex colour map. A library error is returned unchanged.
func run(name, path string) (map[string]any, error) {
	switch name {
	case "github.com/unixpickle/model3d/model3d":
		file, err := os.Open(path)
		if err != nil {
			return nil, err
		}
		defer file.Close()
		triangles, colors, err := model3d.ReadColorPLY(file)
		if err != nil {
			return nil, err
		}
		first := [][]float64{}
		if len(triangles) > 0 {
			for _, c := range triangles[0] {
				first = append(first, []float64{c.X, c.Y, c.Z})
			}
		}
		return map[string]any{"triangles": len(triangles), "first_triangle": first,
			"coloured_vertices": colors.Len()}, nil
	default:
		return nil, fmt.Errorf("unknown ASCII PLY package: %s", name)
	}
}

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL")
	}
	output, err := run(os.Args[1], os.Args[2])
	if err != nil {
		panic(err)
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
