package main

import (
	"bytes"

	"encoding/json"
	"fmt"

	"os"

	"github.com/chenzhekl/goply"
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

	case "github.com/chenzhekl/goply":
		file := goply.New(bytes.NewReader(data))
		output = map[string]any{"vertices": len(file.Elements("vertex")), "faces": len(file.Elements("face"))}

	default:
		panic(fmt.Sprintf("unknown ASCII PLY package: %s", name))
	}
	encoded, err := json.Marshal(output)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
