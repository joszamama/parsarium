// Run one pinned Go WAV parser on the local valid PCM control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"

	youpy "github.com/youpy/go-wav"
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

	case "github.com/youpy/go-wav":
		d := youpy.NewReader(r)
		format, err := d.Format()
		if err != nil {
			return nil, err
		}
		samples, err := d.ReadSamples(4)
		if err != nil {
			return nil, err
		}
		values := make([]int, len(samples))
		for i, sample := range samples {
			values[i] = d.IntValue(sample, 0)
		}
		return map[string]any{"sample_rate": format.SampleRate, "channels": format.NumChannels, "bits": format.BitsPerSample, "signs": signs(values)}, nil

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
