package main

import (
	"encoding/json"
	"fmt"

	"os"

	ajermaky "github.com/ajermaky/assimp-go/v2/asig"
)

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL")
	}
	name, path := os.Args[1], os.Args[2]
	output := map[string]any{}
	switch name {

	case "github.com/ajermaky/assimp-go/v2/asig":
		scene, release, err := ajermaky.ImportFile(path, 0)
		if err != nil {
			panic(err)
		}
		defer release()
		output = map[string]any{"meshes": len(scene.Meshes), "vertices": len(scene.Meshes[0].Vertices), "faces": len(scene.Meshes[0].Faces)}

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
