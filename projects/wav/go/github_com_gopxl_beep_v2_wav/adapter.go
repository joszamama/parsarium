// Run one pinned Go WAV parser on the local valid PCM control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"

	gopxl "github.com/gopxl/beep/v2/wav"
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

	case "github.com/gopxl/beep/v2/wav":
		stream, format, err := gopxl.Decode(r)
		if err != nil {
			return nil, err
		}
		defer stream.Close()
		frames := make([][2]float64, 4)
		n, ok := stream.Stream(frames)
		if !ok && n < 4 {
			return nil, fmt.Errorf("short PCM stream: %d", n)
		}
		values := make([]int, n)
		for i := 0; i < n; i++ {
			if frames[i][0] > 0 {
				values[i] = 1
			} else if frames[i][0] < 0 {
				values[i] = -1
			}
		}
		return map[string]any{"sample_rate": int(format.SampleRate), "channels": format.NumChannels, "signs": values}, nil

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
