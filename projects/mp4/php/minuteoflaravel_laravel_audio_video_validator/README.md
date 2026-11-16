# minuteoflaravel/laravel-audio-video-validator — MP4 / PHP

Pinned release: `1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/mp4/php/minuteoflaravel-laravel-audio-video-validator/README.md)

## Run from the repository root

```sh
python3 parsarium.py build mp4 php minuteoflaravel_laravel_audio_video_validator
python3 parsarium.py run mp4 php minuteoflaravel_laravel_audio_video_validator controls/mp4/red-av.mp4
python3 parsarium.py replay mp4 php minuteoflaravel_laravel_audio_video_validator CORPUS_DIR runs/mp4-minuteoflaravel_laravel_audio_video_validator-replay
python3 parsarium.py afl build mp4 php minuteoflaravel_laravel_audio_video_validator
python3 parsarium.py afl prepare mp4 php minuteoflaravel_laravel_audio_video_validator runs/mp4-minuteoflaravel_laravel_audio_video_validator-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
