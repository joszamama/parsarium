// Run one pinned Go MP3 or ID3v2 parser against the valid tagged MP3 control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"

	"os"

	fgergo "github.com/fgergo/mp3"
)

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	r := bytes.NewReader(data)
	switch name {

	case "github.com/fgergo/mp3":
		decoder := fgergo.NewDecoder(r)
		var frame fgergo.Frame
		var skipped int
		if err := decoder.Decode(&frame, &skipped); err != nil {
			return nil, err
		}
		return map[string]any{"samples": frame.Samples(), "frame_bytes": frame.Size()}, nil

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
