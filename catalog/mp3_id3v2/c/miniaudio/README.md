# miniaudio — MP3 with ID3v2 / C

- **Pinned release:** `0.11.26`
- **License:** LicenseRef-Homebrew-public-domain OR MIT-0
- **Parsed scope:** MP3 audio parsing and decoded PCM from a valid ID3v2-tagged input; tag text is not exposed
- **Underlying family:** miniaudio bundled dr_mp3 decoder
- **Local input API:** `ma_decoder_init_file(local tagged MP3 filename); ma_decoder_read_pcm_frames; ma_decoder_get_length_in_pcm_frames`
- **Documentation:** [API reference](<https://github.com/mackron/miniaudio>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3_id3v2/parsers.json) · [control verification](../../../../data/c/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "sample_rate": 8000,
  "channels": 1,
  "frames": 8000,
  "decoded_frames": 1
}
```

The pinned miniaudio.h embeds dr_mp3 code. C and C++ use the same miniaudio implementation. This is the same dr_mp3 lineage as the excluded SDL3_mixer major release; the library accepts the ID3v2-tagged control but does not expose its title.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
