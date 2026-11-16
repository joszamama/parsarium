# clwu/php-read-mp4info — MP4 / PHP

Pinned release: `v2.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/clwu-php-read-mp4info/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php clwu_php_read_mp4info
python3 parsarium.py run mp4 php clwu_php_read_mp4info controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php clwu_php_read_mp4info CORPUS_DIR runs/mp4-clwu_php_read_mp4info-replay
python3 parsarium.py afl build mp4 php clwu_php_read_mp4info
python3 parsarium.py afl prepare mp4 php clwu_php_read_mp4info runs/mp4-clwu_php_read_mp4info-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
