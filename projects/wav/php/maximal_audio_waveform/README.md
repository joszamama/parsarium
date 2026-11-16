# maximal/audio-waveform — WAV / PHP

Pinned release: `1.2.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/maximal-audio-waveform/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php maximal_audio_waveform
python3 parsarium.py run wav php maximal_audio_waveform controls/wav/256-samples.wav
python3 parsarium.py replay wav php maximal_audio_waveform CORPUS_DIR runs/wav-maximal_audio_waveform-replay
python3 parsarium.py afl build wav php maximal_audio_waveform
python3 parsarium.py afl prepare wav php maximal_audio_waveform runs/wav-maximal_audio_waveform-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
