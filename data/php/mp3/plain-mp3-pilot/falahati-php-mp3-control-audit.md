# falahati/php-mp3 valid-control check

This is a lead check, not a selected or runnable Parsarium path. No fuzzing, malformed inputs or resource tests were used.

## Release and source

Packagist p2 metadata (checked 2026-11-17) lists two tags and `dev-master`:

| Version | Git commit | GitHub zipball SHA-256 |
| --- | --- | --- |
| `v0.9.5-alpha2` (2017-11-01, newest tag, pre-release) | `33ffe2cb6263345aa17f296719e7261e5f351525` | `acb61333616621870cf7c407d0b118674a859cdf3b46c39e0a5cbf4eb0d835fa` |
| `dev-master` commit snapshot (2022-05-12, not a release) | `135aa3010cb4d3412ba442abaf2a7225bb751cf0` | `7376599eb97f970c7c91bdae9e5aebe6a3c58df229985963eac9e7c62f162be3` |

Both are LGPL-3.0 (`LICENSE`, `composer.json`). The package is two classes, `src/MpegAudio.php` and `src/MpegAudioFrameHeader.php`, with no dependency. The snapshot differs from the tag only by a bounds check in `MpegAudio::read()` and an `analyze()` call in `append()`. The upstream README says to install `dev-master`.

## Family

The README says the code is based on [thegallagher/PHP-MP3](https://github.com/thegallagher/PHP-MP3) (`phpmp3.php`, no declared license), which was based on a sourcerally.net script by regin. Both use a `sprintf('%08b')` byte-to-bit-string table and their own bitrate and sample-rate tables. Neither file contains getID3 or Mp3Info code, so this would be a separate regin/PHP-MP3 family. `holine/mp3` copies it.

## Control run

The probe is [`falahati-php-mp3-probe.php`](falahati-php-mp3-probe.php). It calls only `MpegAudio::fromFile()`, `getFrameCounts()`, `getTotalDuration()` and `getFrameHeader($i)` getters. Runtime: PHP 8.5.12 CLI with `error_reporting=0`. Without that setting, PHP prints `Deprecated: Implicit conversion from float 2.5 to int loses precision` for `MpegAudioFrameHeader.php` line 369.

```
php -d error_reporting=0 data/php/mp3/plain-mp3-pilot/falahati-php-mp3-probe.php <package root> controls/mp3/<control>.mp3
```

**Tag v0.9.5-alpha2:** neither control finishes. Both were stopped by `timeout 15` with exit code 124. Since PHP 8.0, `substr()` past the end returns `""` instead of `false`, so the `$byte === false` exit in `getStart()` is never reached after the last frame.

**dev-master 135aa30**, `tone-44k-mono.mp3`:

```
{"frames":11,"duration":0.28725000000000006,"getVersion":1,"getLayerProfile":3,"getSampleRate":44100,"getBitRate":64000,"getChannelMode":3,"getOffset":0,"getLength":208,"frame_offsets":[0,208,417,626,835,1044,1253,1462,1671,1880,2089]}
```

**dev-master 135aa30**, `tone-22k-stereo.mp3`:

```
{"frames":3,"duration":0.3135,"getVersion":2,"getLayerProfile":3,"getSampleRate":11025,"getBitRate":32000,"getChannelMode":1,"getOffset":104,"getLength":418,"frame_offsets":[104,522,940]}
```

`controls/mp3/check_controls.py` reads 11 frames at 44.1 kHz from the first control, and 12 frames at 22.05 kHz from the second. Following its header walk, the frames start at bytes 0, 208, 417, … 2089 in the first control and at 0, 104, 209, 313, 418, 522, … 1149 in the second.

## Results

On the MPEG-1 control, the frame count, sample rate, bitrate, mode (3 = single channel) and frame offsets match the oracle. The duration is the sum of `length × 8 / bitrate` over frames (2,298 × 8 / 64,000). It is not 11 × 1152 / 44,100 = 0.28735 s.

On the MPEG-2 control, the result is wrong in three ways:

- **Sample rate 11,025 instead of 22,050.** `$sampleRateTable` uses the float `Version_25 = 2.5` as an array key. PHP truncates it to `2`, so the MPEG-2.5 row replaces the MPEG-2 row. This happens for every MPEG-2 stream.
- **Frame length 418 instead of 104 or 105.** The length is `144 × bitrate / sampleRate`, the MPEG-1 coefficient (MPEG-2 Layer III uses 72), divided by the halved sample rate.
- **Three frames instead of 12, with the first frame missed.** `getStart()` needs a valid header at `offset + length`. That fails at byte 0 (0 + 418) and succeeds at byte 104 (104 + 418 = 522 lands on a real frame). The last accepted "frame" runs from byte 940 to 1,358, past the 1,254-byte end of the file.

The 0.3135 s duration is close to the byte-based value, but only because these errors cancel. It is not claimed as correct.

The fields that are correct on both controls are MPEG version, layer, bitrate and channel mode. On the MPEG-2 control they come from the second real frame, not the first. Calling `MpegAudioFrameHeader::tryParse()` directly on bytes 0–3 returns `[2, 3, 11025, 32000, 1, 417]` (version, layer, sample rate, bitrate, mode, length), so it has the same sample-rate and length errors. No public API gives a correct first frame, sample rate, frame count, frame bytes or duration on both controls. The lead is recorded as `excluded_control_failed`. Mp3Info was selected with MPEG-1-only scope; that is a different standard and is not applied here.
