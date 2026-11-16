# liferay-mp4parser — MP4 / Java

Pinned release: `1.9.41.2.LIFERAY-PATCHED-2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/java/liferay-mp4parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 java liferay_mp4parser
python3 parsarium.py run mp4 java liferay_mp4parser controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 java liferay_mp4parser CORPUS_DIR runs/mp4-liferay_mp4parser-replay
python3 parsarium.py afl build mp4 java liferay_mp4parser
python3 parsarium.py afl prepare mp4 java liferay_mp4parser runs/mp4-liferay_mp4parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
