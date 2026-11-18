# maximal/audio-waveform — WAV / PHP

- **Pinned release:** `1.2.1`
- **Upstream:** [source repository](<https://github.com/maximal/audio-waveform-php>) · [Packagist](<https://packagist.org/packages/maximal/audio-waveform>)
- **License:** MIT
- **Parsed scope:** Mono WAV sample amplitudes decoded into positive and negative waveform values
- **Underlying family:** SoX native RIFF/WAVE parser
- **Local input API:** `Waveform(local PCM WAV path)->getWaveformData(8); decoded mono amplitude values`
- **Documentation:** [API reference](<https://github.com/maximal/audio-waveform-php/blob/6f513425b83f2d2a0d39b34118f0a1d99ab8d275/readme.md>)
- **Catalog evidence:** [parser record](../../../../data/php/wav/parsers.json) · [control verification](../../../../data/php/wav/verification.json) · [within-ecosystem ranking](../../../../data/php/wav/ranking.md)
- **Valid control:** [`controls/wav/256-samples.wav`](../../../../controls/wav/256-samples.wav)

## Observed control result

```json
{
  "first_channel_samples": 128,
  "second_channel_samples": 0,
  "has_positive_amplitude": true,
  "has_negative_amplitude": true
}
```

Package invokes local SoX to decode PCM samples before constructing waveform data; not an independent WAV decoder.

## Run this target

[Docker harness and verification receipt](../../../../projects/wav/php/maximal_audio_waveform/README.md)

```sh
python3 parsarium.py build wav php maximal_audio_waveform
python3 parsarium.py run wav php maximal_audio_waveform controls/wav/256-samples.wav
```
