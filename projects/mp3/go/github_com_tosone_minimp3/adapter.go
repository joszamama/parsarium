package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"

	"github.com/tosone/minimp3"
)

type summary struct {
	SampleRate   int    `json:"sample_rate"`
	Channels     int    `json:"channels"`
	DecodedBytes int    `json:"decoded_bytes"`
	PCMSHA256    string `json:"pcm_sha256"`
}

func parse(data []byte) (summary, error) {
	if len(data) == 0 {
		return summary{}, fmt.Errorf("empty MP3 input")
	}
	decoder, pcm, err := minimp3.DecodeFull(data)
	if err != nil {
		return summary{}, err
	}
	if decoder == nil {
		return summary{}, fmt.Errorf("decoder returned nil")
	}
	defer decoder.Close()
	if decoder.SampleRate <= 0 || decoder.Channels <= 0 || len(pcm) == 0 {
		return summary{}, fmt.Errorf("no decoded MPEG audio")
	}
	digest := sha256.Sum256(pcm)
	return summary{decoder.SampleRate, decoder.Channels, len(pcm), hex.EncodeToString(digest[:])}, nil
}

func main() {
	if len(os.Args) != 2 {
		panic("usage: adapter CONTROL_PATH")
	}
	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	result, err := parse(data)
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
