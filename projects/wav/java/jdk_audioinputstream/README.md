# AudioSystem.getAudioInputStream(File) — WAV / Java

Pinned release: `21.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/java/wav/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build wav java jdk_audioinputstream
python3 parsarium.py run wav java jdk_audioinputstream controls/wav/256-samples.wav
python3 parsarium.py replay wav java jdk_audioinputstream CORPUS_DIR runs/wav-jdk_audioinputstream-replay
python3 parsarium.py afl build wav java jdk_audioinputstream
python3 parsarium.py afl prepare wav java jdk_audioinputstream runs/wav-jdk_audioinputstream-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
