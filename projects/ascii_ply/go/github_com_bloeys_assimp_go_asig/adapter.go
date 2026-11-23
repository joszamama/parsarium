package main

import (
	"encoding/json"
	"fmt"

	"os"

	bloeys "github.com/bloeys/assimp-go/asig"
)

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL")
	}
	name, path := os.Args[1], os.Args[2]
	output := map[string]any{}
	switch name {

	case "github.com/bloeys/assimp-go/asig":
		scene, release, err := bloeys.ImportFile(path, 0)
		if err != nil {
			panic(err)
		}
		defer release()
		output = map[string]any{"meshes": 0}
		if len(scene.Meshes) > 0 {
			output = map[string]any{"meshes": len(scene.Meshes), "vertices": len(scene.Meshes[0].Vertices), "faces": len(scene.Meshes[0].Faces)}
		}

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
