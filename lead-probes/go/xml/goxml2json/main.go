package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	xml2json "github.com/basgys/goxml2json"
)

func main() {
	if len(os.Args) != 3 {
		panic("expected exactly two XML controls")
	}
	for _, path := range os.Args[1:] {
		data, err := os.ReadFile(path)
		if err != nil {
			panic(err)
		}
		output, err := xml2json.Convert(bytes.NewReader(data))
		if err != nil {
			panic(err)
		}
		var converted any
		if err := json.Unmarshal(output.Bytes(), &converted); err != nil {
			panic(err)
		}
		record := map[string]any{"control": filepath.Base(path), "converted": converted}
		encoded, err := json.Marshal(record)
		if err != nil {
			panic(err)
		}
		fmt.Println(string(encoded))
	}
}
