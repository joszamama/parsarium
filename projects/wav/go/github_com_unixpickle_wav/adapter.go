// Run one pinned Go WAV parser on the local valid PCM control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"

	unixpickle "github.com/unixpickle/wav"
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

	case "github.com/unixpickle/wav":
		parsed, err := unixpickle.NewReader(r)
		if err != nil {
			return nil, err
		}
		values := make([]unixpickle.Sample, 4)
		n, err := parsed.Read(values)
		if err != nil && err != unixpickle.ErrDone {
			return nil, err
		}
		signValues := make([]int, n)
		for i := 0; i < n; i++ {
			if values[i] > 0 {
				signValues[i] = 1
			} else if values[i] < 0 {
				signValues[i] = -1
			}
		}
		return map[string]any{"signs": signValues}, nil

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
