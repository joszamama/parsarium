# opencv — MP4 / C++

- **Pinned release:** `5.1.0`
- **License:** Apache-2.0
- **Parsed scope:** MP4 video dimensions, frame count and frame rate from FFmpeg-backed VideoCapture
- **Underlying family:** OpenCV VideoCapture wrapper over FFmpeg MOV/MP4 demuxer
- **Local input API:** `cv::VideoCapture(local MP4 filename, cv::CAP_FFMPEG); get(CAP_PROP_FRAME_WIDTH/HEIGHT/FRAME_COUNT/FPS)`
- **Documentation:** [API reference](<https://github.com/opencv/opencv/blob/5.1.0/modules/videoio/include/opencv2/videoio.hpp>)
- **Catalog evidence:** [parser record](../../../../data/cpp/mp4/parsers.json) · [control verification](../../../../data/cpp/mp4/verification.json) · [within-ecosystem ranking](../../../../data/cpp/mp4/ranking.md)
- **Valid control:** [`controls/mp4/red-av.mp4`](../../../../controls/mp4/red-av.mp4)

## Observed control result

```json
{
  "width": 2,
  "height": 2,
  "frames": 1,
  "fps": 1
}
```

The pinned libopencv_videoio dylib links the pinned FFmpeg libavformat and libavcodec libraries; this is a distinct C++ package API over the FFmpeg parser family.

## Run this target

[Docker harness and verification receipt](../../../../projects/mp4/cpp/opencv/README.md)

```sh
python3 parsarium.py build mp4 cpp opencv
python3 parsarium.py run mp4 cpp opencv controls/mp4/red-av.mp4
```
