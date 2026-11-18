# PYTHON × WAV: selected parsers

10 control-verified third-party paths selected from 21 verified candidates. The ceiling is ten. A path is an API or package route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

PyPI Stats last_month downloads excluding known mirrors.

| Rank | Package | Release | PyPI downloads (last month) | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html) | 1.18.1 | 292,476,549 | PCM samples | SciPy WAV parser |
| 2 | [av](https://pyav.org/docs/stable/api/container.html) | 19.0.2 | 29,885,680 | PCM samples | FFmpeg libavformat/libavcodec via PyAV |
| 3 | [soundfile](https://python-soundfile.readthedocs.io/en/latest/) | 0.14.0 | 22,760,358 | PCM samples | libsndfile |
| 4 | [pydub](https://github.com/jiaaro/pydub) | 0.25.1 | 17,778,631 | PCM samples | pydub native WAV header parser |
| 5 | [librosa](https://librosa.org/doc/main/api/generated/librosa.load.html) | 1.0.0 | 8,560,686 | PCM samples | librosa via soundfile/libsndfile |
| 6 | [mutagen](https://mutagen.readthedocs.io/en/latest/api/wave.html) | 1.48.1 | 6,946,517 | WAV header/audio metadata | Mutagen WAVE parser |
| 7 | [audioread](https://github.com/beetbox/audioread) | 3.1.0 | 6,117,881 | PCM samples | audioread rawread via CPython wave |
| 8 | [tinytag](https://pypi.org/project/tinytag/2.3.2/) | 2.3.2 | 4,170,323 | WAV header/audio metadata | tinytag RIFF/WAV metadata parser |
| 9 | [pygame](https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound) | 2.6.1 | 2,227,949 | PCM samples | pygame SDL_mixer WAV loader |
| 10 | [pymediainfo](https://pypi.org/project/pymediainfo/7.0.1/) | 7.0.1 | 2,128,669 | WAV header/audio metadata | MediaInfo native WAV parser |

The [selection plan](../../curation/plan.json) records all exclusions and original snapshot hashes. The [metric exception report](../../curation/metric-exceptions.json) lists missing and zero adoption signals. Search limits and unresolved leads remain in `cell.json` and `registry-snapshot.json`.
