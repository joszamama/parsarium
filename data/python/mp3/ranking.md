# Python plain MP3 parser pilot

This pilot has two verified third-party paths. The first is
[`mutagen`](../../../projects/mp3/python/mutagen/README.md) 1.48.1. Its
documented `mutagen.mp3.MP3(fileobj)` API read both untagged MPEG Layer III
controls from an in-memory `BytesIO` and returned the frame-header fields in
`MPEGInfo`: MPEG version, layer, sample rate, channels, bitrate and length. The
package has **10,748,990 PyPI downloads last month** in the
[saved snapshot](registry-snapshot.json). That counts every Mutagen install,
mostly for tags; it is an adoption proxy, not a count of frame-header users.
The same Mutagen package and `mutagen/mp3` module are already counted in the
active Python MP3-with-ID3v2 cell; this is a separate untagged scope, not an
independent parser family.

Mutagen parses headers and checks that following frames sync; it does not
decode audio. With no Xing, Info or VBRI header, as in both controls, it
computes length from the stream size and the first frame's bitrate.

The second is [`tinytag`](../../../projects/mp3/python/tinytag/README.md)
2.3.2, an independent pure-Python reader with **4,453,166 PyPI downloads last
month** (same snapshot; rechecked at 09:04 UTC on 2026-11-17 with the same
value). Its documented `TinyTag.get(file_obj=BytesIO(...))` call sees the
frame sync at byte 0 and hands both untagged controls to its own `_MPEG`
class. The harness rejects any other reader class. On the 44.1 kHz control,
154 TinyTag lines run, 74 of them in `_MPEG` and none in `_ID3`. It returned
sample rate, channels, bitrate (kbit/s) and duration; these match the
[independent header walk](../../../controls/mp3/check_controls.py) for both
controls. TinyTag does not report MPEG version, layer or frame count. After five
frames with the same bitrate it estimates the frame count from the stream size
and their mean length. It does not decode audio.

Both full-length controls run exactly the same TinyTag lines, so they give the
same AFL++ map. The [feedback check](tinytag-valid-feedback.json) therefore
also uses the first three whole frames (626 bytes) of the 44.1 kHz control.
That is still a valid stream, and it ends before the CBR estimate: 16 `_MPEG`
lines and 16 AFL++ tuples change, and repeated runs are identical.

## Primary within-cell adoption metric

PyPI Stats `last_month` downloads excluding known mirrors, captured 2026-11-17.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [mutagen](https://mutagen.readthedocs.io/en/latest/api/mp3.html) | 1.48.1 | 10,748,990 | Layer III frame headers: version, layer, sample rate, channels, bitrate, length | Mutagen MP3/ID3 parser |
| 2 | [tinytag](https://github.com/tinytag/tinytag/blob/2.3.2/README.md#file-like-objects) | 2.3.2 | 4,453,166 | Layer III frame headers: sample rate, channels, bitrate, estimated duration | TinyTag MPEG frame-header reader |

## Leads

Five name queries over the PyPI Simple index returned 123 (`mp3`), 201
(`mpeg`), 2 (`mpg123`), 1 (`minimp3`) and 1 (`layer3`) projects. Download
counts were fetched for 13 named candidates. The [leads](leads.json) record
each one. Only mutagen and tinytag are verified entries.

- av (51,162,307), soundfile (35,041,933), audioread, pygame, pymediainfo and
  miniaudio wrap native decoders (FFmpeg, libsndfile/libmpg123, SDL_mixer,
  MediaInfoLib, dr_mp3). They are unresolved here because Python source
  coverage would not reach their parsers.
- pydub (16,919,511) calls an external ffmpeg binary; excluded.
- librosa (10,902,643) decodes through soundfile or audioread; shared family.
- hachoir, eyed3 and pymp3 are pure-Python leads with their own MPEG header
  code; unresolved, not run.

This two-entry pilot is neither a top-ten ranking nor evidence that only one
Python parser exists. The [cell record](cell.json) gives the remaining
uncertainty, and the [standard-library finding](standard.json) records that
CPython 3.14 documents no MP3 API.
