# github.com/unixpickle/wav — WAV / Go

- **Pinned release:** `v0.0.0-20190525173943-42cf4c455f64`
- **License:** BSD-2-Clause
- **Parsed scope:** signs
- **Underlying family:** unixpickle WAV reader
- **Local input API:** `NewReader(io.Reader); Read([]Sample)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/unixpickle/wav@v0.0.0-20190525173943-42cf4c455f64>)
- **Catalog evidence:** [parser record](../../../../data/go/wav/parsers.json) · [control verification](../../../../data/go/wav/verification.json) · [within-ecosystem ranking](../../../../data/go/wav/ranking.md)
- **Valid control:** [`controls/wav/four-samples.wav`](../../../../controls/wav/four-samples.wav)

## Observed control result

```json
{
  "signs": [
    0,
    1,
    -1,
    0
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
