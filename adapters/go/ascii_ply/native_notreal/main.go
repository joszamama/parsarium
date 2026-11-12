package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/NOT-REAL-GAMES/assimpgo"
)

func main() {
	if len(os.Args) != 2 {
		panic("usage: go run ./native_notreal CONTROL")
	}
	scene, err := assimpgo.ImportFile(os.Args[1], 0)
	if err != nil {
		panic(err)
	}
	defer scene.Release()
	output := map[string]any{"meshes": scene.NumMeshes(), "vertices": scene.Mesh(0).NumVertices(), "faces": len(scene.Mesh(0).Indices()) / 3}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
