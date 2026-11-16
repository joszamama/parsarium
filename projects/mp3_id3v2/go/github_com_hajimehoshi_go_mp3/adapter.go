// Run one pinned Go MP3 or ID3v2 parser against the valid tagged MP3 control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"

	hajime "github.com/hajimehoshi/go-mp3"
)

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	r := bytes.NewReader(data)
	switch name {

	case "github.com/hajimehoshi/go-mp3":
		decoder, err := hajime.NewDecoder(r)
		if err != nil {
			return nil, err
		}
		buf := make([]byte, 64)
		n, err := decoder.Read(buf)
		if err != nil && err != io.EOF {
			return nil, err
		}
		return map[string]any{"sample_rate": decoder.SampleRate(), "decoded_bytes": n}, nil

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
