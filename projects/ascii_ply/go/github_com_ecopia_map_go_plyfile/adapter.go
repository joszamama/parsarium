package main

import (
	"encoding/json"
	"fmt"

	"os"
	"unsafe"

	ecopia "github.com/ecopia-map/go-plyfile"
)

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL")
	}
	name, path := os.Args[1], os.Args[2]
	data, err := os.ReadFile(path)
	if err != nil { panic(err) }
	copy, err := os.CreateTemp("", "parsarium-*.ply")
	if err != nil { panic(err) }
	defer os.Remove(copy.Name())
	if _, err := copy.Write(data); err != nil { copy.Close(); panic(err) }
	if err := copy.Close(); err != nil { panic(err) }
	path = copy.Name()
	output := map[string]any{}
	switch name {

	case "github.com/ecopia-map/go-plyfile":
		file, _ := ecopia.PlyOpenForReading(path)
		defer ecopia.PlyClose(file)
		_, count, _ := ecopia.PlyGetElementDescription(file, "vertex")
		type vertex struct{ X, Y, Z float32 }
		for _, p := range []ecopia.PlyProperty{
			{"x", ecopia.PLY_FLOAT, ecopia.PLY_FLOAT, int(unsafe.Offsetof(vertex{}.X)), 0, 0, 0, 0},
			{"y", ecopia.PLY_FLOAT, ecopia.PLY_FLOAT, int(unsafe.Offsetof(vertex{}.Y)), 0, 0, 0, 0},
			{"z", ecopia.PLY_FLOAT, ecopia.PLY_FLOAT, int(unsafe.Offsetof(vertex{}.Z)), 0, 0, 0, 0},
		} {
			ecopia.PlyGetProperty(file, "vertex", p)
		}
		vertices := make([]vertex, count)
		for i := range vertices {
			ecopia.PlyGetElement(file, &vertices[i], unsafe.Sizeof(vertex{}))
		}
		output = map[string]any{"vertices": len(vertices), "last": vertices[len(vertices)-1]}

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
