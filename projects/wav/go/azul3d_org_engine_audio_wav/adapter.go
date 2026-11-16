// Run one pinned Go WAV parser on the local valid PCM control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"

	azulaudio "azul3d.org/engine/audio"
	_ "azul3d.org/engine/audio/wav"
)

func signs(values []int) []int {
	out := make([]int, len(values))
	for i, value := range values {
		if value > 0 {
			out[i] = 1
		} else if value < 0 {
			out[i] = -1
		}
	}
	return out
}

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	r := bytes.NewReader(data)
	switch name {
	case "azul3d.org/engine/audio/wav":
		decoder, format, err := azulaudio.NewDecoder(r)
		if err != nil {
			return nil, err
		}
		config := decoder.Config()
		return map[string]any{"format": format, "sample_rate": config.SampleRate, "channels": config.Channels}, nil

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
