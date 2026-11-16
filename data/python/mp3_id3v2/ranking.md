# PYTHON × MP3 with ID3v2: selected parsers

10 control-verified third-party paths selected from 20 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

PyPI Stats last_month downloads excluding known mirrors.

| Rank | Package | Release | Metric | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [av](https://pyav.org/docs/stable/api/container.html) | 19.0.2 | 29,885,680 | ID3v2 tags and MP3 audio stream | FFmpeg libavformat via PyAV |
| 2 | [soundfile](https://python-soundfile.readthedocs.io/en/latest/) | 0.14.0 | 22,760,358 | MP3 header, frame count | libsndfile MP3 decoder |
| 3 | [pydub](https://github.com/jiaaro/pydub) | 0.25.1 | 17,778,631 | decoded duration and audio properties | pydub via FFmpeg |
| 4 | [librosa](https://librosa.org/doc/main/api/generated/librosa.load.html) | 1.0.0 | 8,560,686 | decoded PCM sample count | librosa via soundfile/libsndfile |
| 5 | [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) | 0.2.0 | 7,822,402 | ID3v2 tags and MPEG codec | ffmpeg-python via external FFprobe |
| 6 | [mutagen](https://mutagen.readthedocs.io/en/latest/api/wave.html) | 1.48.1 | 6,946,517 | ID3v2 title, artist, album | Mutagen MP3/ID3 parser |
| 7 | [audioread](https://github.com/beetbox/audioread) | 3.1.0 | 6,117,881 | MP3 duration and audio properties | audioread via FFmpeg |
| 8 | [moviepy](https://github.com/Zulko/moviepy/blob/master/moviepy/audio/io/AudioFileClip.py) | 2.2.1 | 4,209,600 | decoded audio and duration | MoviePy via bundled FFmpeg |
| 9 | [tinytag](https://pypi.org/project/tinytag/2.3.2/) | 2.3.2 | 4,170,323 | ID3v2 title, artist, album | TinyTag MP3/ID3 parser |
| 10 | [pygame](https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound) | 2.6.1 | 2,227,949 | decoded audio duration | SDL_mixer MP3 decoder |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
