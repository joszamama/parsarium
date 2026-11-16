package main

import (
	"encoding/json"
	"fmt"

	"os"
	"unsafe"

	cobaltgray "github.com/cobaltgray/go-plyfile"
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

	case "github.com/cobaltgray/go-plyfile":
		file, _ := cobaltgray.PlyOpenForReading(path)
		defer cobaltgray.PlyClose(file)
		_, count, _ := cobaltgray.PlyGetElementDescription(file, "vertex")
		type vertex struct{ X, Y, Z float32 }
		for _, p := range []cobaltgray.PlyProperty{
			{"x", cobaltgray.PLY_FLOAT, cobaltgray.PLY_FLOAT, int(unsafe.Offsetof(vertex{}.X)), 0, 0, 0, 0},
			{"y", cobaltgray.PLY_FLOAT, cobaltgray.PLY_FLOAT, int(unsafe.Offsetof(vertex{}.Y)), 0, 0, 0, 0},
			{"z", cobaltgray.PLY_FLOAT, cobaltgray.PLY_FLOAT, int(unsafe.Offsetof(vertex{}.Z)), 0, 0, 0, 0},
		} {
			cobaltgray.PlyGetProperty(file, "vertex", p)
		}
		vertices := make([]vertex, count)
		for i := range vertices {
			cobaltgray.PlyGetElement(file, &vertices[i], unsafe.Sizeof(vertex{}))
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
