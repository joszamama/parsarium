# libmediainfo — MP3 with ID3v2 / C

- **Pinned release:** `26.10`
- **License:** BSD-2-Clause
- **Parsed scope:** ID3v2 title, MPEG Audio format and 8 kHz sample rate from the tagged MP3
- **Underlying family:** MediaInfoLib MPEG audio and ID3v2 parsers
- **Local input API:** `MediaInfoA_New; MediaInfoA_Open(local filename); MediaInfoA_Get general Title and audio Format/SamplingRate`
- **Documentation:** [API reference](<https://mediaarea.net/en/MediaInfo/Support/SDK/Quick_Start>)
- **Catalog evidence:** [parser record](../../../../data/c/mp3_id3v2/parsers.json) · [control verification](../../../../data/c/mp3_id3v2/verification.json) · [within-ecosystem ranking](../../../../data/c/mp3_id3v2/ranking.md)
- **Valid control:** [`controls/mp3_id3v2/tone-tags.mp3`](../../../../controls/mp3_id3v2/tone-tags.mp3)

## Observed control result

```json
{
  "title": "Parsarium",
  "format": "MPEG Audio",
  "sample_rate": 8000
}
```

Native MediaInfoLib parsers are used from both C and C++ APIs; these call sites share one parser engine across ecosystems. The source has File_Mpega.cpp and File_Id3v2.cpp; its libzen dependency is a base utility library.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
