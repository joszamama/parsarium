package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "os"

    mp3lib "github.com/dmulholl/mp3lib"
)

type summary struct {
    SampleRate *int `json:"sample_rate,omitempty"`
    Channels *int `json:"channels,omitempty"`
    Frames int `json:"frames"`
    FrameBytes int `json:"frame_bytes"`
    SamplesPerFrame *int `json:"samples_per_frame,omitempty"`
    Bitrate *int `json:"bitrate,omitempty"`
}

// same keeps a per-frame property while every frame agrees and drops it when
// the stream changes it from frame to frame (for example a VBR bitrate).
func same(field **int, value int, first bool) {
    if first {
        *field = &value
    } else if *field != nil && **field != value {
        *field = nil
    }
}

// parse walks the frames that the package's stream API returns.
// mp3lib parses frame headers and boundaries; it does not produce PCM.
func parse(data []byte) (summary, error) {
    reader := bytes.NewReader(data)
    var result summary
    varying := map[string]bool{}
    for {
        frame := mp3lib.NextFrame(reader)
        if frame == nil { break }
        channels := 2
        if frame.ChannelMode == mp3lib.Mono { channels = 1 }
        first := result.Frames == 0
        for name, pair := range map[string]struct{ field **int; value int }{
            "sample_rate": {&result.SampleRate, frame.SamplingRate},
            "channels": {&result.Channels, channels},
            "samples_per_frame": {&result.SamplesPerFrame, frame.SampleCount},
            "bitrate": {&result.Bitrate, frame.BitRate},
        } {
            if !varying[name] {
                same(pair.field, pair.value, first)
                varying[name] = *pair.field == nil
            }
        }
        result.Frames++
        result.FrameBytes += frame.FrameLength
    }
    if result.Frames == 0 {
        return summary{}, fmt.Errorf("no MPEG audio frames")
    }
    return result, nil
}

func main() {
    if len(os.Args) != 2 { panic("usage: adapter CONTROL_PATH") }
    data, err := os.ReadFile(os.Args[1]); if err != nil { panic(err) }
    result, err := parse(data); if err != nil { panic(err) }
    if err := json.NewEncoder(os.Stdout).Encode(result); err != nil { panic(err) }
}
