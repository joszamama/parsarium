#include "harness.h"

#include <pointmatcher/IO.h>

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <exception>
#include <fcntl.h>
#include <string>
#include <unistd.h>

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         parsarium_ply_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return false;
    char directory[] = "/tmp/parsarium-libpointmatcher-XXXXXX";
    if (!mkdtemp(directory)) return false;
    std::string path = std::string(directory) + "/input.ply";
    int fd = open(path.c_str(), O_CREAT | O_EXCL | O_WRONLY, 0600);
    if (fd < 0) { rmdir(directory); return false; }
    bool written = true;
    for (std::size_t offset = 0; offset < size;) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { written = false; break; }
        offset += static_cast<std::size_t>(count);
    }
    if (close(fd) != 0) written = false;

    bool okay = false;
    if (written) {
        try {
            const auto cloud = PointMatcherIO<double>::loadPLY(path);
            if (cloud.features.rows() >= 3) {
                result->points = static_cast<std::size_t>(cloud.features.cols());
                result->x_sum = 0;
                result->y_sum = 0;
                result->z_sum = 0;
                for (Eigen::Index i = 0; i < cloud.features.cols(); ++i) {
                    result->x_sum += cloud.features(0, i);
                    result->y_sum += cloud.features(1, i);
                    result->z_sum += cloud.features(2, i);
                }
                okay = std::isfinite(result->x_sum) &&
                       std::isfinite(result->y_sum) &&
                       std::isfinite(result->z_sum);
            }
        } catch (const std::exception &) {
            // A rejected input remains an ordinary fuzzer iteration.
        }
    }
    unlink(path.c_str());
    rmdir(directory);
    return okay;
}
