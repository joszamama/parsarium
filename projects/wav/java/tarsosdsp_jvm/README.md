# tarsosdsp-jvm — WAV / Java

Pinned release: `2.5`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/wav/java/tarsosdsp-jvm/README.md)

## Run from the repository root

```sh
python3 parsarium.py build wav java tarsosdsp_jvm
python3 parsarium.py run wav java tarsosdsp_jvm controls/wav/256-samples.wav
python3 parsarium.py replay wav java tarsosdsp_jvm CORPUS_DIR runs/wav-tarsosdsp_jvm-replay
python3 parsarium.py afl build wav java tarsosdsp_jvm
python3 parsarium.py afl prepare wav java tarsosdsp_jvm runs/wav-tarsosdsp_jvm-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Feedback covers TarsosDSP JVM and core classes. The WAV decoder underneath is Java Sound in the JDK and is not included in the package-source line count.
