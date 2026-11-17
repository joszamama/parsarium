package main

import (
	"encoding/json"
	"fmt"
	"os"

	"go.viam.com/rdk/spatialmath"
)

// The documented spatialmath.NewMeshFromPLYFile(path) reads the PLY through
// goply and converts each three-index face into a millimetre-scaled triangle.
func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL")
	}
	name, path := os.Args[1], os.Args[2]
	output := map[string]any{}
	switch name {

	case "go.viam.com/rdk/spatialmath":
		mesh, err := spatialmath.NewMeshFromPLYFile(path)
		if err != nil {
			fmt.Println(`{"error":"rejected"}`)
			return
		}
		triangles := mesh.Triangles()
		first := [][]float64{}
		if len(triangles) > 0 {
			for _, point := range triangles[0].Points() {
				first = append(first, []float64{point.X, point.Y, point.Z})
			}
		}
		output = map[string]any{"triangles": len(triangles), "first_triangle_mm": first}

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
