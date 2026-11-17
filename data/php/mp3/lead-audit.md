# PHP plain MP3 lead checks

These are lead checks, not selected or runnable Parsarium paths. Each package was read at the commit Packagist p2 metadata lists for its newest version (checked 2026-11-17). Runs used only the two valid controls in `controls/mp3/` and the probe [`lead-probes.php`](lead-probes.php). No fuzzing, malformed inputs or resource tests were used. The header walk in `controls/mp3/check_controls.py` reads 11 frames, 44,100 Hz, mono, 64 kbit/s from `tone-44k-mono.mp3` and 12 frames, 22,050 Hz, stereo, 32 kbit/s from `tone-22k-stereo.mp3`.

None of these leads is promoted. The cell stays at two selected paths.

## debach/zend-mp3 1.8.1 (45,227 downloads)

Commit `17b523ad57f283ddf3a116bc0eff22cb9d1b4b27`, BSD-3-Clause (`composer.json`). This is the pinned release that `projects/mp3_id3v2/php/debach_zend_mp3` installs from Packagist and checks against the codeload archive (SHA-256 `2cf59be0e16a25ff6369bada6c1e6f739a47f7eda6da3c3abc59a7e899c9ef38`).

The package does parse MPEG audio frames itself, beyond ID3. The README documents `new Zend_Media_Mpeg_Abs('file.mp3')` with `getLengthEstimate()` and `getLength()`. `Zend_Media_Mpeg_Abs_Frame` searches for the 11-bit sync, decodes version, layer, bitrate, sample rate, padding and mode from its own tables, computes each frame length with separate MPEG-1 (144) and MPEG-2 (72) Layer III coefficients, and skips to the next frame. `Zend_Media_Mpeg_Abs::_readFrames()` walks every frame. The fork caps that walk at 200 frames, which does not affect the 11- and 12-frame controls.

It cannot load on PHP 8. `Zend_Media_Mpeg_Abs` extends `Zend_Media_Mpeg_Abs_Object`, which extends `Zend_Media_Mpeg_Object`. That file uses `$buffer{$pos++}` string offsets (line 144), a syntax PHP 8.0 removed. `Mpeg/Abs/VbriHeader.php` line 88 has an unparenthesized nested ternary, a fatal error since PHP 8.0. In the image built from `projects/mp3_id3v2/php/debach_zend_mp3` (PHP 8.5.4, the same base as the selected PHP MP3 paths):

```
php -l /work/vendor/debach/zend-mp3/lib/Zend/Media/Mpeg/Object.php
PHP Parse error:  syntax error, unexpected token "{", expecting ")" in .../Zend/Media/Mpeg/Object.php on line 144
php -l /work/vendor/debach/zend-mp3/lib/Zend/Media/Mpeg/Abs/VbriHeader.php
PHP Fatal error:  Unparenthesized `a ? b : c ? d : e` is not supported. ... on line 88
php lead-probes.php zend /work/vendor/debach/zend-mp3 <both controls>    # exit 255, same parse error
```

The ID3v2 reader counted in the MP3-with-ID3v2 cell does not load these files, so it still runs. Patching the release is outside the protocol. There is no newer Packagist version. No PHP 8.5 API returns a frame-level result, so the lead is recorded as `excluded_control_failed`.

## fobilow/mp3file dev-master (5,468 downloads)

Packagist lists only `dev-master` (commit `5e0f5c7da8804a149a2bb1ca89c45ec8ea7e0388`, 2013-08-22) and no release tag. `composer.json` declares no license and `LICENSE` is an empty file. The single class `Mp3File` (Zedwood's script) reads the first frame header bit by bit and derives CBR duration from file size and header bitrate. Its frame size uses the MPEG-1 coefficient 144 for every version. It does not walk frames.

On PHP 8.5.12, `Mp3File.php` does not compile: `$mp3['MPEG version']{1}` at line 253 is a removed string-offset syntax (`Parse error: syntax error, unexpected token "{"`, exit 255 on both controls). The lead fails the release, license and control gates and is recorded as `excluded_control_failed`.

## xiaosongshu/flv2mp4 v1.8.7 (190 downloads)

This was excluded by its package description, which names FLV/MP4/HLS conversion. A re-scan of the snapshot found that it contains a native PHP MPEG Layer III decoder. Commit `9e84aaf8b8d74e2965b451622dce02e9fa206728` (2026-11-12) is Apache-2.0. `src/Mp3/Mp3L3Decoder.php` (1,203 lines) syncs on frame headers, decodes side info, Huffman data and synthesis, and returns planar samples.

The README documents only `Client::runMp32Wav($in, $out)`. That call runs `Manage\AudioParallelPipeline`, which uses `proc_open` to start `bin/audio-worker.php` in a separate PHP process. In-process parser-line coverage would not see the decoder. `Manage\Mp32Pcm` calls the decoder in-process but is not documented.

The decoder accepts only MPEG-1 Layer III: `decode()` skips every header whose version ID is not 3. On PHP 8.5.12, `Mp3L3Decoder::decode()` gives:

```
tone-44k-mono.mp3   {"sampleRate":44100,"channels":1,"samples_per_channel":[12672]}
tone-22k-stereo.mp3 {"sampleRate":0,"channels":0,"samples_per_channel":[0]}
```

On the MPEG-1 control, 12,672 samples are 11 × 1,152, so the result matches the oracle's 11 frames, sample rate and channel count. On the MPEG-2 control it decodes no frames, where the oracle reads 12. The lead is recorded as `excluded_control_failed`. The documented API also runs out of process.

## holine/mp3 0.0.1 (9 downloads)

Commit `ea924ae7392a5ba916a639e2b33080a36e9929e5`, LGPL-3.0. After whitespace and namespace are removed, `src/MpegAudio.php` and `src/MpegAudioFrameHeader.php` differ from falahati/php-mp3 only in brace placement and `namespace MP3`. They keep the `Version_25 = 2.5` float array key that breaks MPEG-2 sample rates ([falahati audit](falahati-php-mp3-control-audit.md)). With `falahati-php-mp3-probe.php` retargeted to `\MP3\MpegAudio`, neither control returns within `timeout 15` on PHP 8.5.12 (exit 124), the same as the falahati v0.9.5-alpha2 tag. The lead is recorded as `excluded_control_failed`, in the PHP-MP3 family.

## Wrappers and other reclassifications

- **wapmorgan/media-file 0.1.4** (248,980; commit `263f773696e02d173fb9636c9a8111ac84032292`, MIT). `src/Adapters/Mp3Adapter.php` constructs `wapmorgan\Mp3Info\Mp3Info($filename)` and returns its `duration`, `bitRate`, `sampleRate`, `channel` and `isVbr` properties. It has no MPEG code of its own. `MediaFile` picks the adapter with `wapmorgan/file-type-detector`. Its `composer.json` requires `wapmorgan/mp3info ~0.0`, and the MP3-with-ID3v2 project lock resolves this to 0.1.1, the selected release. The lead is recorded as `shared_family`.
- **buggedcom/phpvideotoolkit 2.2.5** (89,411; commit `383a5b2c0ee7f4de4efea9a9154bb693630bbe0f`). Media information comes from `MediaProbeParser`/`MediaParser`, which build `ffprobe`/`ffmpeg` command lines through `FfmpegProcess` and `ExecBuffer`. `Mime.php` reads only a few bytes for MIME sniffing. No in-process MPEG parser exists. The lead is recorded as `excluded_native_wrapper`, with no build.
- **acekyd/laravelmp3 1.0.3** (3,711; commit `28a870499a489fe7da8ce84aba2ffa62903a4d68`, GPL-2.0). It bundles getID3 `1.9.5-20130220` in `src/getid3/` and calls `new \getID3` with `analyze()`. The lead is recorded as `shared_family` (getID3); its composer.json requires `php ^5.3.3 || ^7.0`.
- **akiosarkiz/mp3php 1.2.0** (598; commit `7de9da29519a34c05632a36a24f7d9bf541884e6`, MIT). `src/Mp3.php` runs `ffprobe -show_format -show_streams` through `shell_exec`. The lead is recorded as `excluded_native_wrapper`.
- **phpmlkit/soundfile 1.2.0** (20) binds libsndfile through `ext-ffi` (`include/sndfile.h`), so parsing happens in native C. **nicoverbruggen/mediaprobe v1.1** (6) runs `exec("ffprobe ...")`. Both are recorded as `excluded_native_wrapper`.
- **dgoriaev/mp3info 1.0.3** (6; LGPL-3.0). After whitespace is removed, `src/Mp3Info.php` matches Mp3Info 0.1.1 except for its namespace and a three-line early return. The lead is recorded as `shared_family`.
- **stinger-soft/media-parsing-bundle** (27, dev-master only) requires `phansys/getid3`. **orkan/winamp** (9) requires `james-heinrich/getid3`. Both stay outside the cell (no release, or CLI tools).
- **rheck/mp3-bundle** (68) has its own frame-header handler, but Packagist lists only `dev-master` and it requires `symfony/symfony 2.3.*`. **jamshidbekakhlidinov/php-mp3** (0, dev-main only) is a copy of thegallagher PHP-MP3, with the same `sprintf('%08b')` table. Both stay `excluded` because no release exists.
