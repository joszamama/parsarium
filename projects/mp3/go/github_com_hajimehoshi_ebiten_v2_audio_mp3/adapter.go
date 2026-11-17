// Decode one untagged MPEG audio Layer III stream through the pinned Ebitengine MP3 wrapper.
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"

	"github.com/hajimehoshi/ebiten/v2/audio/mp3"
)

const maxDecodedBytes = 64 << 20

func run(name, path string) (map[string]any, error) {
	if name != "github.com/hajimehoshi/ebiten/v2/audio/mp3" {
		return nil, fmt.Errorf("unknown package %q", name)
	}
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	// The plain MP3 pilot accepts bare MPEG audio frames only; tagged inputs
	// belong to mp3_id3v2.
	if bytes.HasPrefix(data, []byte("ID3")) {
		return nil, errors.New("ID3v2 tag present")
	}
	if len(data) >= 128 && bytes.HasPrefix(data[len(data)-128:], []byte("TAG")) {
		return nil, errors.New("ID3v1 tag present")
	}
	// DecodeWithoutResampling needs no audio context and keeps the stream's
	// own sample rate; it returns 16-bit little-endian stereo PCM.
	stream, err := mp3.DecodeWithoutResampling(bytes.NewReader(data))
	if err != nil {
		return nil, err
	}
	digest := sha256.New()
	decoded, err := io.Copy(digest, io.LimitReader(stream, maxDecodedBytes))
	if err != nil {
		return nil, err
	}
	if decoded == 0 {
		return nil, errors.New("no decoded PCM")
	}
	return map[string]any{
		"sample_rate":   stream.SampleRate(),
		"length_bytes":  stream.Length(),
		"decoded_bytes": decoded,
		"pcm_sha256":    hex.EncodeToString(digest.Sum(nil)),
	}, nil
}

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE INPUT_PATH")
	}
	result, err := run(os.Args[1], os.Args[2])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
