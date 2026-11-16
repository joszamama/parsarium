# kiwilan/php-audio — WAV / PHP

Pinned release: `4.0.02`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/php/kiwilan-php-audio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav php kiwilan_php_audio
python3 parsarium.py run wav php kiwilan_php_audio controls/wav/256-samples.wav
python3 parsarium.py replay wav php kiwilan_php_audio CORPUS_DIR runs/wav-kiwilan_php_audio-replay
python3 parsarium.py afl build wav php kiwilan_php_audio
python3 parsarium.py afl prepare wav php kiwilan_php_audio runs/wav-kiwilan_php_audio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
