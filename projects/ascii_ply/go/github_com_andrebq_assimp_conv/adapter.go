package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/andrebq/assimp/conv"
)

// run reads the PLY with conv.LoadAsset, which imports the file with Assimp
// (aiImportFile) and converts the C scene to Go meshes. A library error is
// returned unchanged.
func run(path string) (map[string]any, error) {
	scene, err := conv.LoadAsset(path)
	if err != nil {
		return nil, err
	}
	if len(scene.Mesh) == 0 {
		return map[string]any{"meshes": 0}, nil
	}
	mesh := scene.Mesh[0]
	return map[string]any{"meshes": len(scene.Mesh), "vertices": len(mesh.Vertices), "faces": len(mesh.Faces)}, nil
}

func main() {
	if len(os.Args) != 2 {
		panic("usage: adapter CONTROL")
	}
	result, err := run(os.Args[1])
	if err != nil {
		panic(err)
	}
	encoded, err := json.Marshal(result)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
