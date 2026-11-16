package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"

	"os"

	glutter "github.com/rm4n0s/glutter/model/ply"
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

	case "github.com/rm4n0s/glutter/model/ply":
		model, err := glutter.Decode(context.Background(), bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		output = map[string]any{"meshes": len(model.Meshes), "faces": model.TriangleCount()}

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
