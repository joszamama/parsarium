#include "harness.h"
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <cstring>
#include <unistd.h>

bool parse_data(const std::uint8_t *data, std::size_t size, Result *result) {
    static constexpr std::uint8_t png_signature[] = {137, 80, 78, 71, 13, 10, 26, 10};
    if (!data || !result || size < sizeof(png_signature) || size > (1u << 20)
        || std::memcmp(data, png_signature, sizeof(png_signature)) != 0) return false;
    std::memset(result, 0, sizeof(*result));
    char path[] = "/tmp/parsarium-XXXXXX.png";
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
        const cv::Mat image = cv::imread(path, cv::IMREAD_UNCHANGED);
        if (!image.empty() && image.cols >= 1 && image.rows >= 1) {
            result->width = static_cast<unsigned>(image.cols);
            result->height = static_cast<unsigned>(image.rows);
            // Pixel samples are supplementary observations. A valid decoded
            // PNG still succeeds when it has one column or a non-8-bit depth.
            if (image.depth() == CV_8U && image.channels() >= 1 && image.channels() <= 4) {
                const auto *row = image.ptr<std::uint8_t>(0);
                const int channels = image.channels();
                const auto sample = [channels](const std::uint8_t *pixel, std::uint8_t *rgba) {
                    if (channels <= 2) {
                        rgba[0] = rgba[1] = rgba[2] = pixel[0];
                        rgba[3] = channels == 2 ? pixel[1] : 255;
                    } else {
                        // OpenCV exposes colour pixels in BGR(A) order.
                        rgba[0] = pixel[2]; rgba[1] = pixel[1]; rgba[2] = pixel[0];
                        rgba[3] = channels == 4 ? pixel[3] : 255;
                    }
                };
                sample(row, result->first);
                result->has_first = true;
                if (image.cols >= 2) {
                    sample(row + channels, result->second);
                    result->has_second = true;
                }
            }
            ok = true;
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
