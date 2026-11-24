// Run one pinned Go WAV parser on the local valid PCM control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"

	klang "github.com/200sc/klangsynthese/wav"
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

	case "github.com/200sc/klangsynthese/wav":
		parsed, err := klang.Read(r)
		if err != nil {
			return nil, err
		}
		// Read takes the 44-byte canonical header layout without checking chunk
		// IDs. When it returns no channels or a zero sample rate it read no
		// audio format from the file; that is a rejection, not a zero format.
		if parsed.NumChannels == 0 || parsed.SampleRate == 0 {
			return nil, fmt.Errorf("klangsynthese read no audio format: %d channels, sample rate %d", parsed.NumChannels, parsed.SampleRate)
		}
		return map[string]any{"sample_rate": parsed.SampleRate, "channels": parsed.NumChannels, "bits": parsed.BitsPerSample, "data_bytes": len(parsed.Data)}, nil

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
