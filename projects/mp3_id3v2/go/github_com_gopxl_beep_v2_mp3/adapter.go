// Run one pinned Go MP3 or ID3v2 parser against the valid tagged MP3 control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"

	gopxl "github.com/gopxl/beep/v2/mp3"
)

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	r := bytes.NewReader(data)
	switch name {

	case "github.com/gopxl/beep/v2/mp3":
		stream, format, err := gopxl.Decode(io.NopCloser(r))
		if err != nil {
			return nil, err
		}
		defer stream.Close()
		samples := make([][2]float64, 16)
		n, ok := stream.Stream(samples)
		if !ok && n == 0 {
			return nil, fmt.Errorf("no decoded samples")
		}
		return map[string]any{"sample_rate": int(format.SampleRate), "samples": n}, nil

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
