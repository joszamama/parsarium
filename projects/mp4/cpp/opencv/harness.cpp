#include "harness.h"
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <cmath>
#include <cstring>
#include <unistd.h>

bool parse_data(const std::uint8_t *data, std::size_t size, Result *result) {
    // MP4 scope: an ISO BMFF file whose first box is ftyp. The FFmpeg build
    // only registers the mov demuxer, so other containers are rejected anyway.
    if (!data || !result || size < 8 || size > (1u << 20)
        || std::memcmp(data + 4, "ftyp", 4) != 0) return false;
    std::memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-opencv-XXXXXX.mp4";
    int fd = mkstemps(path, 4);
    if (fd < 0) return false;
    std::size_t offset = 0;
    while (offset < size) {
        ssize_t n = write(fd, data + offset, size - offset);
        if (n <= 0) { close(fd); unlink(path); return false; }
        offset += static_cast<std::size_t>(n);
    }
    close(fd);
    bool ok = false;
    try {
        cv::VideoCapture video(path, cv::CAP_FFMPEG);
        if (video.isOpened()) {
            result->width = video.get(cv::CAP_PROP_FRAME_WIDTH);
            result->height = video.get(cv::CAP_PROP_FRAME_HEIGHT);
            result->frames = video.get(cv::CAP_PROP_FRAME_COUNT);
            result->fps = video.get(cv::CAP_PROP_FPS);
            ok = true;
            for (double value : {result->width, result->height, result->frames, result->fps})
                ok = ok && std::isfinite(value) && value >= 0 && value < 1e15;
        }
    } catch (const cv::Exception &) {
        ok = false;
    }
    unlink(path);
    return ok;
}

extern "C" int LLVMFuzzerTestOneInput(const std::uint8_t *data, std::size_t size) {
    Result result{};
    (void)parse_data(data, size, &result);
    return 0;
}
