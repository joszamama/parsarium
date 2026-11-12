# C × WAV: verified parser ranking

5 verified third-party package paths; working goal 20, ceiling 30. The metric is GitHub repository stars captured at 2026-11-12T10:25:21.715408+00:00. The captured Conan Center recipe-name surface provides no comparable per-recipe download counts. Stars are a repository-level adoption proxy, compared only within C, and do not establish a complete most-used set. 0 path(s) lack a metric and remain unranked.

Search hits, unresolved leads, and the C standard-library inventory are separate. See `cell.json`, `registry-snapshot.json`, `leads.json`, `standard.json`, and `verification.json`.

| Rank | Package | Pinned release | Repository stars | Scope | Underlying family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [ffmpeg](https://ffmpeg.org/doxygen/9.0/group__lavf__decoding.html) | 9.0.2 | 67,107 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | FFmpeg WAV demuxer and PCM decoder |
| 2 | [raylib](https://github.com/raysan5/raylib/blob/6.2/src/raylib.h) | 6.2 | 35,640 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | raylib bundled dr_wav decoder |
| 3 | [miniaudio](https://github.com/mackron/miniaudio/blob/0.11.26/miniaudio.h) | 0.11.26 | 7,616 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | miniaudio bundled dr_wav decoder |
| 4 | [dr_wav](https://github.com/mackron/dr_libs/blob/wav-0.14.6/dr_wav.h) | wav-0.14.6 | 1,891 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | dr_wav C WAV decoder |
| 5 | [libsndfile](https://libsndfile.github.io/libsndfile/api.html) | 1.2.2 | 1,732 | WAV sample rate, channel and frame counts, plus first four decoded PCM samples | libsndfile WAV decoder |
