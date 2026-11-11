// Run one pinned Go WAV parser on the local valid PCM control.
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"

	azulaudio "azul3d.org/engine/audio"
	_ "azul3d.org/engine/audio/wav"
	klang "github.com/200sc/klangsynthese/wav"
	cryptix "github.com/cryptix/wav"
	cwbudde "github.com/cwbudde/wav"
	faiface "github.com/faiface/beep/wav"
	goaudio "github.com/go-audio/wav"
	gonutz "github.com/gonutz/mixer/wav"
	gopxl "github.com/gopxl/beep/v2/wav"
	ebiten "github.com/hajimehoshi/ebiten/v2/audio/wav"
	godub "github.com/iFaceless/godub/wav"
	inky "github.com/inkyblackness/res/audio/wav"
	mattetti "github.com/mattetti/audio/wav"
	moutend "github.com/moutend/go-wav"
	ngyewch "github.com/ngyewch/go-pcm/wav"
	qiniu "github.com/qiniu/audio/wav"
	"github.com/tphakala/go-wav/pcm"
	unixpickle "github.com/unixpickle/wav"
	weakpixel "github.com/weakpixel/voice/wav"
	wavreader "github.com/xigh/go-wavreader"
	youpy "github.com/youpy/go-wav"
	"github.com/yut-kt/gowave"
)

func signs(values []int) []int {
	out := make([]int, len(values))
	for i, value := range values {
		if value > 0 {
			out[i] = 1
		} else if value < 0 {
			out[i] = -1
		}
	}
	return out
}

func run(name, path string) (map[string]any, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	r := bytes.NewReader(data)
	switch name {
	case "azul3d.org/engine/audio/wav":
		decoder, format, err := azulaudio.NewDecoder(r)
		if err != nil {
			return nil, err
		}
		config := decoder.Config()
		return map[string]any{"format": format, "sample_rate": config.SampleRate, "channels": config.Channels}, nil
	case "github.com/inkyblackness/res/audio/wav":
		decoded, err := inky.Load(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": decoded.SampleRate(), "sample_count": decoded.SampleCount()}, nil
	case "github.com/weakpixel/voice/wav":
		samples, rate, err := weakpixel.Read(r)
		if err != nil {
			return nil, err
		}
		values := make([]int, len(samples))
		for i, value := range samples {
			if value > 0 {
				values[i] = 1
			} else if value < 0 {
				values[i] = -1
			}
		}
		return map[string]any{"sample_rate": rate, "signs": values}, nil
	case "github.com/ngyewch/go-pcm/wav":
		reader, err := ngyewch.NewReader(path)
		if err != nil {
			return nil, err
		}
		defer reader.Close()
		buffer := make([]byte, 8)
		n, err := reader.Read(buffer)
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": reader.SampleRate(), "channels": reader.NumChannels(), "data_bytes": n}, nil
	case "github.com/go-audio/wav":
		d := goaudio.NewDecoder(r)
		if !d.IsValidFile() {
			return nil, fmt.Errorf("invalid WAV")
		}
		buf, err := d.FullPCMBuffer()
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": d.SampleRate, "channels": d.NumChans, "bits": d.BitDepth, "signs": signs(buf.Data)}, nil
	case "github.com/faiface/beep/wav":
		stream, format, err := faiface.Decode(r)
		if err != nil {
			return nil, err
		}
		defer stream.Close()
		frames := make([][2]float64, 4)
		n, ok := stream.Stream(frames)
		if !ok && n < 4 {
			return nil, fmt.Errorf("short PCM stream: %d", n)
		}
		values := make([]int, n)
		for i := 0; i < n; i++ {
			if frames[i][0] > 0 {
				values[i] = 1
			} else if frames[i][0] < 0 {
				values[i] = -1
			}
		}
		return map[string]any{"sample_rate": int(format.SampleRate), "channels": format.NumChannels, "signs": values}, nil
	case "github.com/gopxl/beep/v2/wav":
		stream, format, err := gopxl.Decode(r)
		if err != nil {
			return nil, err
		}
		defer stream.Close()
		frames := make([][2]float64, 4)
		n, ok := stream.Stream(frames)
		if !ok && n < 4 {
			return nil, fmt.Errorf("short PCM stream: %d", n)
		}
		values := make([]int, n)
		for i := 0; i < n; i++ {
			if frames[i][0] > 0 {
				values[i] = 1
			} else if frames[i][0] < 0 {
				values[i] = -1
			}
		}
		return map[string]any{"sample_rate": int(format.SampleRate), "channels": format.NumChannels, "signs": values}, nil
	case "github.com/hajimehoshi/ebiten/v2/audio/wav":
		stream, err := ebiten.DecodeWithoutResampling(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": stream.SampleRate(), "decoded_stereo_bytes": stream.Length()}, nil
	case "github.com/cryptix/wav":
		d, err := cryptix.NewReader(r, int64(len(data)))
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": d.GetSampleRate(), "channels": d.GetNumChannels(), "bits": d.GetBitsPerSample(), "sample_count": d.GetSampleCount()}, nil
	case "github.com/youpy/go-wav":
		d := youpy.NewReader(r)
		format, err := d.Format()
		if err != nil {
			return nil, err
		}
		samples, err := d.ReadSamples(4)
		if err != nil {
			return nil, err
		}
		values := make([]int, len(samples))
		for i, sample := range samples {
			values[i] = d.IntValue(sample, 0)
		}
		return map[string]any{"sample_rate": format.SampleRate, "channels": format.NumChannels, "bits": format.BitsPerSample, "signs": signs(values)}, nil
	case "github.com/moutend/go-wav":
		var file moutend.File
		if err := moutend.Unmarshal(data, &file); err != nil {
			return nil, err
		}
		values := make([]int, len(file.Int32s()))
		for i, value := range file.Int32s() {
			values[i] = int(value)
		}
		return map[string]any{"sample_rate": file.SamplesPerSec(), "channels": file.Channels(), "bits": file.BitsPerSample(), "signs": signs(values)}, nil
	case "github.com/mattetti/audio/wav":
		d := mattetti.NewDecoder(r)
		if !d.IsValidFile() {
			return nil, fmt.Errorf("invalid WAV")
		}
		buf, err := d.FullPCMBuffer()
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": d.SampleRate, "channels": d.NumChans, "bits": d.BitDepth, "signs": signs(buf.AsInts())}, nil
	case "github.com/200sc/klangsynthese/wav":
		parsed, err := klang.Read(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": parsed.SampleRate, "channels": parsed.NumChannels, "bits": parsed.BitsPerSample, "data_bytes": len(parsed.Data)}, nil
	case "github.com/iFaceless/godub/wav":
		parsed, err := godub.Decode(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": parsed.SampleRate, "channels": parsed.Channels, "bits": parsed.BitsPerSample, "data_bytes": len(parsed.RawData)}, nil
	case "github.com/cwbudde/wav":
		d := cwbudde.NewDecoder(r)
		if !d.IsValidFile() {
			return nil, fmt.Errorf("invalid WAV")
		}
		buf, err := d.FullPCMBuffer()
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": d.SampleRate, "channels": d.NumChans, "bits": d.BitDepth, "sample_count": len(buf.Data)}, nil
	case "github.com/qiniu/audio/wav":
		decoded, err := qiniu.Decode(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": decoded.SampleRate(), "channels": decoded.Channels(), "decoded_bytes": decoded.Length()}, nil
	case "github.com/xigh/go-wavreader":
		d, err := wavreader.New(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": d.Rate(), "channels": d.Chans(), "frames": d.Len()}, nil
	case "github.com/gonutz/mixer/wav":
		parsed, err := gonutz.Read(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": parsed.SamplesPerSecond, "channels": parsed.ChannelCount, "bits": parsed.BitsPerSample, "data_bytes": len(parsed.Data)}, nil
	case "github.com/yut-kt/gowave":
		parsed, err := gowave.New(r)
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": parsed.GetSampleRate(), "channels": parsed.GetNumChannels()}, nil
	case "github.com/unixpickle/wav":
		parsed, err := unixpickle.NewReader(r)
		if err != nil {
			return nil, err
		}
		values := make([]unixpickle.Sample, 4)
		n, err := parsed.Read(values)
		if err != nil && err != unixpickle.ErrDone {
			return nil, err
		}
		signValues := make([]int, n)
		for i := 0; i < n; i++ {
			if values[i] > 0 {
				signValues[i] = 1
			} else if values[i] < 0 {
				signValues[i] = -1
			}
		}
		return map[string]any{"signs": signValues}, nil
	case "github.com/tphakala/go-wav/pcm":
		decoded, info, err := pcm.DecodeInterleavedBytes(data)
		if err != nil {
			return nil, err
		}
		return map[string]any{"sample_rate": info.SampleRate, "channels": info.Channels, "bits": info.BitDepth, "data_bytes": len(decoded)}, nil
	default:
		return nil, fmt.Errorf("unknown package %q", name)
	}
}

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run . PACKAGE CONTROL_PATH")
	}
	result, err := run(os.Args[1], os.Args[2])
	if err != nil {
		panic(err)
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
