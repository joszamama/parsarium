// Run one pinned Go MP3 or ID3v2 parser against the valid tagged MP3 control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"

	"os"

	bogem "github.com/bogem/id3v2/v2"
)

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	r := bytes.NewReader(data)
	switch name {

	case "github.com/bogem/id3v2/v2":
		metadata, err := bogem.ParseReader(r, bogem.Options{Parse: true})
		if err != nil {
			return nil, err
		}
		return map[string]any{"title": metadata.Title()}, nil

	default:
		return nil, fmt.Errorf("unknown package %q", name)
	}
}

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL_PATH")
	}
	result, err := run(os.Args[1], os.Args[2])
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
