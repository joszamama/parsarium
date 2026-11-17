# mp3-duration — plain MP3 / JavaScript

**Verified frame-derived duration path in an incomplete format cell.** This package is selected for its documented `mp3Duration(Buffer, false)` API. With `cbrEstimate` disabled, its own `index.js` walks MPEG frame headers, advances by each calculated frame length, and sums samples divided by sample rate. It returns duration only; it does not expose frames or decoded audio.

- **Pinned release:** 1.1.0 (MIT), [source](https://github.com/ddsol/mp3-duration/tree/20bda6406e92ad200f5774d3a88ae2d9dc1e2cbc) and [API](https://github.com/ddsol/mp3-duration/blob/20bda6406e92ad200f5774d3a88ae2d9dc1e2cbc/README.md).
- **Adoption:** 43,261 npm downloads in the saved 30-day period, 2026-10-17 to 2026-11-15. Counts include transitive use and are comparable only within the JavaScript snapshot.
- **Controls:** [MPEG-1 mono](../../../../controls/mp3/tone-44k-mono.mp3) and [MPEG-2 stereo](../../../../controls/mp3/tone-22k-stereo.mp3).
- **Evidence:** [parser record](../../../../data/javascript/mp3/parsers.json), [source lock](../../../../projects/mp3/javascript/mp3_duration/source-lock.json), [Docker control receipt](../../../../projects/mp3/javascript/mp3_duration/verification.json), [AFL++ feedback](../../../../data/javascript/mp3/mp3_duration-feedback-differential.json).

The package returns 287 ms and 313 ms on the two untagged controls. The independent [frame-header walker](../../../../controls/mp3/check_controls.py) counts 11 frames at 1152 samples/44.1 kHz and 12 frames at 576 samples/22.05 kHz; rounding each frame-derived duration to milliseconds gives the same results. The package's README calls the value seconds; the pinned source confirms that unit and rounds it to the nearest millisecond. The harness converts seconds to an integer millisecond result.

The control replay covers 156 lines of `mp3-duration/index.js`. AFL++ feedback is scoped to V8 source ranges in its `parseFrameHeader` and `frameSize` functions, with exact hit counts capped at 255. Three fresh replays of each valid control agree; the functions execute 11 and 12 times respectively, and a module load without parsing has zero parser features. **This feedback reflects frame-count execution and may track input length. It is not a new branch or line-coverage claim.** The default source-range bridge for other JavaScript projects is unchanged.

The same package and release are verified in the separate MP3-with-ID3v2 cell for a tagged file's duration; this is a distinct untagged-input format path, not a new parser family. Two short CBR controls do not establish VBR, free-format, Layer I/II, MPEG-2.5 or ID3 behavior. No malformed-input, resource-use, or fuzz campaign was run.

## Run

```sh
python3 parsarium.py build mp3 javascript mp3_duration
python3 parsarium.py run mp3 javascript mp3_duration controls/mp3/tone-44k-mono.mp3
python3 parsarium.py run mp3 javascript mp3_duration controls/mp3/tone-22k-stereo.mp3
python3 parsarium.py replay mp3 javascript mp3_duration CORPUS_DIR runs/mp3-mp3-duration-replay
python3 parsarium.py afl build mp3 javascript mp3_duration
python3 parsarium.py afl prepare mp3 javascript mp3_duration runs/mp3-mp3-duration-afl
```

The AFL++ preparation command seeds a run and does not start a campaign.
