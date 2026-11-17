// Run one pinned Go MP3 or ID3v2 parser against the valid tagged MP3 control.
package main

import (
	"encoding/json"
	"fmt"

	"os"

	"github.com/tosone/minimp3"
)

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	switch name {

	case "github.com/tosone/minimp3":
		decoder, decoded, err := minimp3.DecodeFull(data)
		if err != nil {
			return nil, err
		}
		defer decoder.Close()
		return map[string]any{"sample_rate": decoder.SampleRate, "channels": decoder.Channels, "decoded_bytes": len(decoded)}, nil

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
