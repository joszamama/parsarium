# Python plain MP3 parser pilot

The only verified third-party path in this pilot is
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

## Primary within-cell adoption metric

PyPI Stats `last_month` downloads excluding known mirrors, captured 2026-11-17.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [mutagen](https://mutagen.readthedocs.io/en/latest/api/mp3.html) | 1.48.1 | 10,748,990 | Layer III frame headers: version, layer, sample rate, channels, bitrate, length | Mutagen MP3/ID3 parser |

## Leads

Five name queries over the PyPI Simple index returned 123 (`mp3`), 201
(`mpeg`), 2 (`mpg123`), 1 (`minimp3`) and 1 (`layer3`) projects. Download
counts were fetched for 13 named candidates. The [leads](leads.json) record
each one. None is a verified entry.

- av (51,162,307), soundfile (35,041,933), audioread, pygame, pymediainfo and
  miniaudio wrap native decoders (FFmpeg, libsndfile/libmpg123, SDL_mixer,
  MediaInfoLib, dr_mp3). They are unresolved here because Python source
  coverage would not reach their parsers.
- pydub (16,919,511) calls an external ffmpeg binary; excluded.
- librosa (10,902,643) decodes through soundfile or audioread; shared family.
- tinytag (4,453,166), hachoir, eyed3 and pymp3 are pure-Python leads with
  their own MPEG header code; unresolved, not run.

This one-entry pilot is neither a top-ten ranking nor evidence that only one
Python parser exists. The [cell record](cell.json) gives the remaining
uncertainty, and the [standard-library finding](standard.json) records that
CPython 3.14 documents no MP3 API.
