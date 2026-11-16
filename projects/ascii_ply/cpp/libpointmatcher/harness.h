#ifndef PARSARIUM_LIBPOINTMATCHER_PLY_HARNESS_H
#define PARSARIUM_LIBPOINTMATCHER_PLY_HARNESS_H

#include <cstddef>
#include <cstdint>

struct parsarium_ply_result {
    std::size_t points;
    double x_sum;
    double y_sum;
    double z_sum;
};

bool parsarium_parse_ply(const std::uint8_t *data, std::size_t size,
                         parsarium_ply_result *result);

#endif
