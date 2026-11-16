// Run one pinned Go PDF reader against the valid, one-page local control.
package main

import (
	"bytes"

	"encoding/json"
	"fmt"

	"os"

	seehuhn "seehuhn.de/go/pdf"
)

func run(name string, data []byte) (map[string]any, error) {
	r := bytes.NewReader(data)
	pageCount := 0
	var err error
	switch name {

	case "seehuhn.de/go/pdf":
		doc, openErr := seehuhn.NewReader(r, int64(len(data)), nil)
		err = openErr
		if err == nil {
			defer doc.Close()
			return map[string]any{"version": doc.GetMeta().Version.String()}, nil
		}

	default:
		return nil, fmt.Errorf("unknown package %q", name)
	}
	if err != nil {
		return nil, err
	}
	return map[string]any{"pages": pageCount}, nil
}

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL_PATH")
	}
	data, err := os.ReadFile(os.Args[2])
	if err != nil {
		panic(err)
	}
	result, err := run(os.Args[1], data)
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
