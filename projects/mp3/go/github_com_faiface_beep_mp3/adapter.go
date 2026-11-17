// Decode one untagged MPEG audio Layer III stream through the pinned Beep MP3 wrapper.
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math"
	"os"

	"github.com/faiface/beep/mp3"
)

const maxSamples = 16 << 20

// readSeekNopCloser gives Decode a seekable io.ReadCloser, so the wrapped
// go-mp3 decoder scans every frame for Len().
type readSeekNopCloser struct{ io.ReadSeeker }

func (readSeekNopCloser) Close() error { return nil }

func run(name, path string) (map[string]any, error) {
	if name != "github.com/faiface/beep/mp3" {
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
	streamer, format, err := mp3.Decode(readSeekNopCloser{bytes.NewReader(data)})
	if err != nil {
		return nil, err
	}
	defer streamer.Close()
	digest := sha256.New()
	buffer := make([][2]float64, 512)
	var word [8]byte
	streamed := 0
	for streamed < maxSamples {
		n, ok := streamer.Stream(buffer)
		for _, sample := range buffer[:n] {
			for _, channel := range sample {
				binary.LittleEndian.PutUint64(word[:], math.Float64bits(channel))
				digest.Write(word[:])
			}
		}
		streamed += n
		if !ok {
			break
		}
	}
	if err := streamer.Err(); err != nil {
		return nil, err
	}
	if streamed == 0 {
		return nil, errors.New("no decoded samples")
	}
	return map[string]any{
		"sample_rate":      int(format.SampleRate),
		"length_samples":   streamer.Len(),
		"streamed_samples": streamed,
		"samples_sha256":   hex.EncodeToString(digest.Sum(nil)),
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
