package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"unsafe"

	arf "github.com/ARF-DEV/assimp-go/asig"
	bhaumik "github.com/BhaumikTalwar/assimp-go/asig"
	polyform "github.com/EliCDavis/polyform/formats/ply"
	ajermaky "github.com/ajermaky/assimp-go/v2/asig"
	bruteray "github.com/barnex/bruteray/tracer/objects/ply"
	bloeys "github.com/bloeys/assimp-go/asig"
	"github.com/borud/pointcloud"
	"github.com/chenzhekl/goply"
	cobaltgray "github.com/cobaltgray/go-plyfile"
	ecopia "github.com/ecopia-map/go-plyfile"
	matching "github.com/malcolmston/opencv/surface_matching"
	dedalo "github.com/pydpll/dedalo/obj"
	rishabh "github.com/rishabh-bector/assimp-golang"
	glutter "github.com/rm4n0s/glutter/model/ply"
	"github.com/thebanri/limoni/graphics"
	"github.com/unixpickle/model3d/fileformats"
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
	case "github.com/EliCDavis/polyform/formats/ply":
		mesh, err := polyform.ReadMesh(bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		output = map[string]any{"vertices": mesh.AttributeLength(), "faces": mesh.PrimitiveCount()}
	case "github.com/rm4n0s/glutter/model/ply":
		model, err := glutter.Decode(context.Background(), bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		output = map[string]any{"meshes": len(model.Meshes), "faces": model.TriangleCount()}
	case "github.com/chenzhekl/goply":
		file := goply.New(bytes.NewReader(data))
		output = map[string]any{"vertices": len(file.Elements("vertex")), "faces": len(file.Elements("face"))}
	case "github.com/thebanri/limoni/graphics":
		model, err := graphics.ParsePLY(bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		output = map[string]any{"vertices": len(model.Vertices), "faces": len(model.Faces)}
	case "nimbleterminal.dev/nt3d/mesh":
		model, err := nt3dmesh.DecodePLY(data, nil)
		if err != nil {
			panic(err)
		}
		output = map[string]any{"objects": len(model.Objects), "faces": model.Triangles()}
	case "github.com/malcolmston/opencv/surface_matching":
		cloud, err := matching.LoadPLY(path)
		if err != nil {
			panic(err)
		}
		output = map[string]any{"vertices": cloud.Len(), "first": cloud.Points[0]}
	case "github.com/borud/pointcloud":
		cloud, err := pointcloud.ReadPLY(bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		output = map[string]any{"vertices": len(cloud.Points), "bounds": []float64{cloud.MinX, cloud.MaxX, cloud.MinY, cloud.MaxY}}
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
	case "github.com/ecopia-map/go-plyfile":
		file, _ := ecopia.PlyOpenForReading(path)
		defer ecopia.PlyClose(file)
		_, count, _ := ecopia.PlyGetElementDescription(file, "vertex")
		type vertex struct{ X, Y, Z float32 }
		for _, p := range []ecopia.PlyProperty{
			{"x", ecopia.PLY_FLOAT, ecopia.PLY_FLOAT, int(unsafe.Offsetof(vertex{}.X)), 0, 0, 0, 0},
			{"y", ecopia.PLY_FLOAT, ecopia.PLY_FLOAT, int(unsafe.Offsetof(vertex{}.Y)), 0, 0, 0, 0},
			{"z", ecopia.PLY_FLOAT, ecopia.PLY_FLOAT, int(unsafe.Offsetof(vertex{}.Z)), 0, 0, 0, 0},
		} {
			ecopia.PlyGetProperty(file, "vertex", p)
		}
		vertices := make([]vertex, count)
		for i := range vertices {
			ecopia.PlyGetElement(file, &vertices[i], unsafe.Sizeof(vertex{}))
		}
		output = map[string]any{"vertices": len(vertices), "last": vertices[len(vertices)-1]}
	case "github.com/rishabh-bector/assimp-golang":
		scene := rishabh.ImportFileFromMemory(data, 0, "ply")
		if scene == nil {
			panic("Assimp import failed")
		}
		defer scene.ReleaseImport()
		output = map[string]any{"meshes": scene.NumMeshes(), "vertices": scene.Meshes()[0].NumVertices(), "faces": scene.Meshes()[0].NumFaces()}
	case "github.com/bloeys/assimp-go/asig":
		scene, release, err := bloeys.ImportFile(path, 0)
		if err != nil {
			panic(err)
		}
		defer release()
		output = map[string]any{"meshes": len(scene.Meshes), "vertices": len(scene.Meshes[0].Vertices), "faces": len(scene.Meshes[0].Faces)}
	case "github.com/ajermaky/assimp-go/v2/asig":
		scene, release, err := ajermaky.ImportFile(path, 0)
		if err != nil {
			panic(err)
		}
		defer release()
		output = map[string]any{"meshes": len(scene.Meshes), "vertices": len(scene.Meshes[0].Vertices), "faces": len(scene.Meshes[0].Faces)}
	case "github.com/unixpickle/model3d/fileformats":
		reader, err := fileformats.NewPLYReader(bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		counts := map[string]int{}
		for {
			_, element, err := reader.Read()
			if err == io.EOF {
				break
			}
			if err != nil {
				panic(err)
			}
			counts[element.Name]++
		}
		output = map[string]any{"vertices": counts["vertex"], "faces": counts["face"]}
	case "github.com/ARF-DEV/assimp-go/asig":
		scene, release, err := arf.ImportFile(path, 0)
		if err != nil {
			panic(err)
		}
		defer release()
		output = map[string]any{"meshes": len(scene.Meshes), "vertices": len(scene.Meshes[0].Vertices), "faces": len(scene.Meshes[0].Faces)}
	case "github.com/BhaumikTalwar/assimp-go/asig":
		scene, release, err := bhaumik.ImportFile(path, 0)
		if err != nil {
			panic(err)
		}
		defer release()
		output = map[string]any{"meshes": len(scene.Meshes), "vertices": len(scene.Meshes[0].Vertices), "faces": len(scene.Meshes[0].Faces)}
	case "github.com/pydpll/dedalo/obj":
		mesh, err := dedalo.ParsePLY(bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		output = map[string]any{"vertices": mesh.NumVertices(), "faces": mesh.NumFaces()}
	case "github.com/barnex/bruteray/tracer/objects/ply":
		vertices, faces, err := bruteray.Parse(bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		output = map[string]any{"vertices": len(vertices), "faces": len(faces)}
	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
