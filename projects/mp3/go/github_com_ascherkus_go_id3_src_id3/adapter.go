// Run one pinned Go MP3 or ID3v2 parser against the valid tagged MP3 control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"

	"os"

	ascherkus "github.com/ascherkus/go-id3/src/id3"
)

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	r := bytes.NewReader(data)
	switch name {

	case "github.com/ascherkus/go-id3/src/id3":
		metadata := ascherkus.Read(r)
		if metadata == nil {
			return nil, fmt.Errorf("no ID3v2 metadata")
		}
		return map[string]any{"title": metadata.Name}, nil

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
