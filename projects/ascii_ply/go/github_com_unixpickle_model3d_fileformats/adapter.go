package main

import (
	"bytes"

	"encoding/json"
	"fmt"
	"io"
	"os"

	"github.com/unixpickle/model3d/fileformats"
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

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
