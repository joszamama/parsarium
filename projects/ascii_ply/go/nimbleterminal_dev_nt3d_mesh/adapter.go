package main

import (
	"encoding/json"
	"fmt"

	"os"

	nt3dmesh "nimbleterminal.dev/nt3d/mesh"
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

	case "nimbleterminal.dev/nt3d/mesh":
		model, err := nt3dmesh.DecodePLY(data, nil)
		if err != nil {
			panic(err)
		}
		output = map[string]any{"objects": len(model.Objects), "faces": model.Triangles()}

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
