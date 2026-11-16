# kiwilan/php-audio — MP4 / PHP

Pinned release: `4.0.02`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/kiwilan-php-audio/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php kiwilan_php_audio
python3 parsarium.py run mp4 php kiwilan_php_audio controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php kiwilan_php_audio CORPUS_DIR runs/mp4-kiwilan_php_audio-replay
python3 parsarium.py afl build mp4 php kiwilan_php_audio
python3 parsarium.py afl prepare mp4 php kiwilan_php_audio runs/mp4-kiwilan_php_audio-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
