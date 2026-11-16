package main

import (
	"encoding/json"
	"fmt"

	"os"

	rishabh "github.com/rishabh-bector/assimp-golang"
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

	case "github.com/rishabh-bector/assimp-golang":
		scene := rishabh.ImportFileFromMemory(data, 0, "ply")
		if scene == nil {
			panic("Assimp import failed")
		}
		defer scene.ReleaseImport()
		output = map[string]any{"meshes": scene.NumMeshes(), "vertices": scene.Meshes()[0].NumVertices(), "faces": scene.Meshes()[0].NumFaces()}

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
