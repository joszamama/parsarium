package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "os"

    mp3 "github.com/tcolgate/mp3"
)

type summary struct {
    SampleRate int `json:"sample_rate"`
    Channels int `json:"channels"`
    Frames int `json:"frames"`
    FrameBytes int `json:"frame_bytes"`
    SamplesPerFrame int `json:"samples_per_frame"`
    Bitrate int `json:"bitrate"`
}

// parse reads complete MPEG Layer III frames through the package decoder.
// This package parses frames and side information; it does not produce PCM.
func parse(data []byte) (summary, error) {
    decoder := mp3.NewDecoder(bytes.NewReader(data))
    var result summary
    for {
        var frame mp3.Frame
        var skipped int
        err := decoder.Decode(&frame, &skipped)
        if err == io.EOF {
            break
        }
        if err != nil {
            return summary{}, err
        }
        if skipped != 0 {
            return summary{}, fmt.Errorf("skipped %d bytes before frame", skipped)
        }
        header := frame.Header()
        if header.Layer() != mp3.Layer3 {
            return summary{}, fmt.Errorf("input contains non-Layer-III frame")
        }
        channels := 2
        if header.ChannelMode() == mp3.SingleChannel {
            channels = 1
        }
        rate, bitrate, samples := int(header.SampleRate()), int(header.BitRate()), frame.Samples()
        if result.Frames == 0 {
            result.SampleRate, result.Channels = rate, channels
            result.SamplesPerFrame, result.Bitrate = samples, bitrate
        } else if result.SampleRate != rate || result.Channels != channels || result.SamplesPerFrame != samples || result.Bitrate != bitrate {
            return summary{}, fmt.Errorf("control frames disagree")
        }
        result.Frames++
        result.FrameBytes += frame.Size()
    }
    if result.Frames == 0 || result.FrameBytes != len(data) {
        return summary{}, fmt.Errorf("no complete frames or trailing bytes: %d of %d", result.FrameBytes, len(data))
    }
    return result, nil
}

func main() {
    if len(os.Args) != 2 {
        panic("usage: adapter CONTROL_PATH")
    }
    data, err := os.ReadFile(os.Args[1])
    if err != nil { panic(err) }
    result, err := parse(data)
    if err != nil { panic(err) }
    if err := json.NewEncoder(os.Stdout).Encode(result); err != nil { panic(err) }
}
