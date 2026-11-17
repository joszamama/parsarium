# PYTHON × MP3: selected parsers

10 control-verified third-party paths selected from 11 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

PyPI Stats last_month downloads excluding known mirrors.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [av](https://pyav.org/docs/stable/api/container.html) | 19.0.2 | 51,162,307 | ID3v2 tags and MP3 audio stream | FFmpeg libavformat via PyAV |
| 2 | [soundfile](https://python-soundfile.readthedocs.io/en/latest/) | 0.14.0 | 35,041,933 | MP3 header, frame count | libsndfile MP3 decoder |
| 3 | [pydub](https://github.com/jiaaro/pydub) | 0.25.1 | 16,919,511 | decoded duration and audio properties | pydub via FFmpeg |
| 4 | [librosa](https://librosa.org/doc/main/api/generated/librosa.load.html) | 1.0.0 | 10,902,643 | decoded PCM sample count | librosa via soundfile/libsndfile |
| 5 | [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) | 0.2.0 | 10,769,281 | ID3v2 tags and MPEG codec | ffmpeg-python via external FFprobe |
| 6 | [mutagen](https://mutagen.readthedocs.io/en/latest/api/wave.html) | 1.48.1 | 10,748,990 | ID3v2 title, artist, album | Mutagen MP3/ID3 parser |
| 7 | [audioread](https://github.com/beetbox/audioread) | 3.1.0 | 7,283,376 | MP3 duration and audio properties | audioread via FFmpeg |
| 8 | [moviepy](https://github.com/Zulko/moviepy/blob/master/moviepy/audio/io/AudioFileClip.py) | 2.2.1 | 5,465,948 | decoded audio and duration | MoviePy via bundled FFmpeg |
| 9 | [tinytag](https://pypi.org/project/tinytag/2.3.2/) | 2.3.2 | 4,453,166 | ID3v2 title, artist, album | TinyTag MP3/ID3 parser |
| 10 | [pygame](https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound) | 2.6.1 | 2,704,018 | decoded audio duration | SDL_mixer MP3 decoder |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
