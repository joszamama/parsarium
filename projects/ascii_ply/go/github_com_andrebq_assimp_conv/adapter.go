package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/andrebq/assimp/conv"
)

func main() {
	if len(os.Args) != 2 {
		panic("usage: adapter CONTROL")
	}
	// conv.LoadAsset imports the file with Assimp (aiImportFile) and converts the C scene to Go meshes.
	// A file the importer rejects (for example a point cloud without faces) is reported, not raised.
	scene, err := conv.LoadAsset(os.Args[1])
	result := map[string]any{"meshes": 0}
	if err != nil {
		result["error"] = "assimp import failed"
	} else if len(scene.Mesh) > 0 {
		mesh := scene.Mesh[0]
		result = map[string]any{"meshes": len(scene.Mesh), "vertices": len(mesh.Vertices), "faces": len(mesh.Faces)}
	}
	encoded, err := json.Marshal(result)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
