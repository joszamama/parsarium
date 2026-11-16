package main

import (
	"encoding/json"
	"fmt"
	"os"

	assimp "github.com/tbogdala/assimp-go"
)

func main() {
	if len(os.Args) != 2 {
		panic("usage: go run ./native_tbogdala CONTROL")
	}
	meshes, err := assimp.ParseFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	encoded, err := json.Marshal(map[string]any{"meshes": len(meshes), "vertices": meshes[0].VertexCount, "faces": meshes[0].FaceCount})
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
