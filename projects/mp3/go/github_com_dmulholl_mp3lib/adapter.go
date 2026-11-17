package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "os"

    mp3lib "github.com/dmulholl/mp3lib"
)

type summary struct {
    SampleRate int `json:"sample_rate"`
    Channels int `json:"channels"`
    Frames int `json:"frames"`
    FrameBytes int `json:"frame_bytes"`
    SamplesPerFrame int `json:"samples_per_frame"`
    Bitrate int `json:"bitrate"`
}

// parse walks complete untagged Layer III frames using the package's stream API.
// mp3lib parses frame headers and boundaries; it does not produce PCM.
func parse(data []byte) (summary, error) {
    reader := bytes.NewReader(data)
    var result summary
    for {
        frame := mp3lib.NextFrame(reader)
        if frame == nil { break }
        if frame.MPEGLayer != mp3lib.MPEGLayerIII {
            return summary{}, fmt.Errorf("input contains non-Layer-III frame")
        }
        channels := 2
        if frame.ChannelMode == mp3lib.Mono { channels = 1 }
        bitrate := frame.BitRate
        if result.Frames == 0 {
            result.SampleRate, result.Channels = frame.SamplingRate, channels
            result.SamplesPerFrame, result.Bitrate = frame.SampleCount, bitrate
        } else if result.SampleRate != frame.SamplingRate || result.Channels != channels || result.SamplesPerFrame != frame.SampleCount || result.Bitrate != bitrate {
            return summary{}, fmt.Errorf("control frames disagree")
        }
        result.Frames++
        result.FrameBytes += frame.FrameLength
    }
    if result.Frames == 0 || result.FrameBytes != len(data) || reader.Len() != 0 {
        return summary{}, fmt.Errorf("no complete frames or trailing bytes: %d of %d", result.FrameBytes, len(data))
    }
    return result, nil
}

func main() {
    if len(os.Args) != 2 { panic("usage: adapter CONTROL_PATH") }
    data, err := os.ReadFile(os.Args[1]); if err != nil { panic(err) }
    result, err := parse(data); if err != nil { panic(err) }
    if err := json.NewEncoder(os.Stdout).Encode(result); err != nil { panic(err) }
}
