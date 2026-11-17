// Walk one untagged MPEG audio Layer III stream with the pinned mattetti/audio/mp3 Decoder.Next.
package main

import (
	"bytes"
	"errors"
	"fmt"
	"io"
	"os"

	"github.com/mattetti/audio/mp3"
)

type summary struct {
	SampleRate      int `json:"sample_rate"`
	Channels        int `json:"channels"`
	Frames          int `json:"frames"`
	FrameBytes      int `json:"frame_bytes"`
	SamplesPerFrame int `json:"samples_per_frame"`
	Bitrate         int `json:"bitrate"`
}

func parse(path string) (summary, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return summary{}, err
	}
	decoder := mp3.New(bytes.NewReader(data))
	var result summary
	frame := &mp3.Frame{}
	for {
		err := decoder.Next(frame)
		if err == io.EOF {
			break
		}
		if err != nil {
			return summary{}, err
		}
		if frame.SkippedBytes != 0 {
			return summary{}, fmt.Errorf("skipped %d bytes", frame.SkippedBytes)
		}
		h := frame.Header
		if h.Layer() != mp3.Layer3 {
			return summary{}, errors.New("non-Layer-III frame")
		}
		channels := 2
		if h.ChannelMode() == mp3.SingleChannel {
			channels = 1
		}
		rate, bitrate, samples := int(h.SampleRate()), int(h.BitRate()), h.Samples()
		if result.Frames == 0 {
			result.SampleRate, result.Channels, result.SamplesPerFrame, result.Bitrate = rate, channels, samples, bitrate
		} else if result.SampleRate != rate || result.Channels != channels || result.SamplesPerFrame != samples || result.Bitrate != bitrate {
			return summary{}, errors.New("frames disagree")
		}
		result.Frames++
		result.FrameBytes += int(h.Size())
	}
	if result.Frames == 0 || result.FrameBytes != len(data) {
		return summary{}, fmt.Errorf("frames %d bytes %d of %d", result.Frames, result.FrameBytes, len(data))
	}
	return result, nil
}
