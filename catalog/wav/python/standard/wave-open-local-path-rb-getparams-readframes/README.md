# wave.open(local path, 'rb'); getparams(); readframes() — WAV / Python

- **Runtime:** CPython 3.13.1 standard library
- **Input API:** `wave.open(local path, 'rb'); getparams(); readframes()`
- **Official documentation:** [reference](https://docs.python.org/3.13/library/wave.html)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../../controls/wav/four-samples.wav)
- **Inventory and verification:** [standard API record](../../../../../data/python/wav/standard.json) · [saved result](../../../../../data/python/wav/verification.json)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "bits_per_sample": 16,
  "samples": [
    0,
    1000,
    -1000,
    0
  ]
}
```

[Control adapter](../../../../../adapters/python/wav/standard.py)

## Run this target

```sh
python3 parsarium.py build wav python stdlib_wave
python3 parsarium.py run wav python stdlib_wave controls/wav/four-samples.wav
```
