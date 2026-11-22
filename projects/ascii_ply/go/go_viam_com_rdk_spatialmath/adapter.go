package main

import (
	"encoding/json"
	"fmt"
	"os"

	"go.viam.com/rdk/spatialmath"
)

// run reads the PLY with the documented spatialmath.NewMeshFromPLYFile(path),
// which reads it through goply and converts each three-index face into a
// millimetre-scaled triangle. A library error is returned unchanged.
func run(name, path string) (map[string]any, error) {
	switch name {
	case "go.viam.com/rdk/spatialmath":
		mesh, err := spatialmath.NewMeshFromPLYFile(path)
		if err != nil {
			return nil, err
		}
		triangles := mesh.Triangles()
		first := [][]float64{}
		if len(triangles) > 0 {
			for _, point := range triangles[0].Points() {
				first = append(first, []float64{point.X, point.Y, point.Z})
			}
		}
		return map[string]any{"triangles": len(triangles), "first_triangle_mm": first}, nil
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
