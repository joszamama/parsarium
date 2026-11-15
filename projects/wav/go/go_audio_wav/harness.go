package wavharness

import (
	"bytes"
	"errors"

	"github.com/go-audio/wav"
)

type Result struct {
	SampleRate int   `json:"sample_rate"`
	Channels   int   `json:"channels"`
	Bits       int   `json:"bits"`
	Signs      []int `json:"signs"`
}

func Parse(data []byte) (Result, error) {
	if len(data) == 0 || len(data) > 1<<20 {
		return Result{}, errors.New("input outside harness limit")
	}
	decoder := wav.NewDecoder(bytes.NewReader(data))
	buffer, err := decoder.FullPCMBuffer()
	if err != nil {
		return Result{}, err
	}
	result := Result{SampleRate: int(decoder.SampleRate), Channels: int(decoder.NumChans),
		Bits: int(decoder.BitDepth), Signs: make([]int, 0, 4)}
	for _, sample := range buffer.Data {
		if len(result.Signs) == 4 {
			break
		}
		sign := 0
		if sample > 0 {
			sign = 1
		} else if sample < 0 {
			sign = -1
		}
		result.Signs = append(result.Signs, sign)
	}
	return result, nil
}
