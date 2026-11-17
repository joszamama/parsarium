package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"

	"github.com/korandiz/mpa"
)

type result struct {
	Control  string `json:"control"`
	SHA256   string `json:"sha256"`
	Frames   int    `json:"frames"`
	RateHz   int    `json:"rate_hz"`
	Channels int    `json:"channels"`
	Samples  int    `json:"samples"`
	End      string `json:"end"`
}

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "usage: go run . CONTROL.mp3 [CONTROL.mp3 ...]")
		os.Exit(2)
	}
	results := make([]result, 0, len(os.Args)-1)
	for _, path := range os.Args[1:] {
		data, err := os.ReadFile(path)
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
		sum := sha256.Sum256(data)
		r := result{Control: filepath.Base(path), SHA256: hex.EncodeToString(sum[:])}
		decoder := &mpa.Decoder{Input: bytes.NewReader(data)}
		for {
			err := decoder.DecodeFrame()
			if err == io.EOF {
				r.End = "EOF"
				break
			}
			if err != nil {
				r.End = err.Error()
				break
			}
			r.Frames++
			r.RateHz = decoder.SamplingFrequency()
			r.Channels = decoder.NChannels()
			r.Samples += decoder.NSamples()
		}
		results = append(results, r)
	}
	if err := json.NewEncoder(os.Stdout).Encode(results); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
