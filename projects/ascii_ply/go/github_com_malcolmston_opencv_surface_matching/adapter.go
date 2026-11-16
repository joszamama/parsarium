package main

import (
	"encoding/json"
	"fmt"

	"os"

	matching "github.com/malcolmston/opencv/surface_matching"
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

	case "github.com/malcolmston/opencv/surface_matching":
		cloud, err := matching.LoadPLY(path)
		if err != nil {
			panic(err)
		}
		output = map[string]any{"vertices": cloud.Len(), "first": cloud.Points[0]}

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
