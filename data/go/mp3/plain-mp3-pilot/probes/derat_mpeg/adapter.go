// Walk one untagged MPEG audio Layer III stream with the pinned derat/mpeg frame-header reader.
package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"os"

	"github.com/derat/mpeg"
)

type summary struct {
	SampleRate      int `json:"sample_rate"`
	Channels        int `json:"channels"`
	Frames          int `json:"frames"`
	FrameBytes      int `json:"frame_bytes"`
	SamplesPerFrame int `json:"samples_per_frame"`
	Bitrate         int `json:"bitrate"`
}

// parse reads each frame header with mpeg.ReadFrameInfo and advances by the
// package-computed FrameInfo.Size until the file ends exactly on a frame boundary.
func parse(path string) (summary, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return summary{}, err
	}
	if bytes.HasPrefix(data, []byte("ID3")) {
		return summary{}, errors.New("ID3v2 tag present")
	}
	if len(data) >= 128 && bytes.HasPrefix(data[len(data)-128:], []byte("TAG")) {
		return summary{}, errors.New("ID3v1 tag present")
	}
	file, err := os.Open(path)
	if err != nil {
		return summary{}, err
	}
	defer file.Close()
	size := int64(len(data))
	var result summary
	for offset := int64(0); offset < size; {
		info, err := mpeg.ReadFrameInfo(file, offset)
		if err != nil {
			return summary{}, fmt.Errorf("frame at byte %d: %w", offset, err)
		}
		length := info.Size()
		if length < 4 || offset+length > size {
			return summary{}, fmt.Errorf("incomplete frame at byte %d", offset)
		}
		channels := 2
		if info.ChannelMode == 0x3 {
			channels = 1
		}
		if result.Frames == 0 {
			result.SampleRate, result.Channels = info.SampleRate, channels
			result.SamplesPerFrame, result.Bitrate = info.SamplesPerFrame, info.KbitRate*1000
		} else if result.SampleRate != info.SampleRate || result.Channels != channels ||
			result.SamplesPerFrame != info.SamplesPerFrame || result.Bitrate != info.KbitRate*1000 {
			return summary{}, fmt.Errorf("frame at byte %d changes stream parameters", offset)
		}
		result.Frames++
		result.FrameBytes += int(length)
		offset += length
	}
	if result.Frames == 0 {
		return summary{}, errors.New("no MPEG audio frames")
	}
	return result, nil
}

func main() {
	if len(os.Args) != 2 {
		panic("usage: adapter INPUT_PATH")
	}
	result, err := parse(os.Args[1])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
