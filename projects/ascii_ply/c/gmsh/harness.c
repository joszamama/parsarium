#define _GNU_SOURCE
#include "harness.h"

#include <gmshc.h>

#include <math.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result) {
    if (!data || !result || size == 0 || size > (1u << 20)) return 0;
    char directory[] = "/tmp/parsarium-gmsh-XXXXXX";
    if (!mkdtemp(directory)) return 0;
    char path[sizeof(directory) + sizeof("/input.ply")];
    snprintf(path, sizeof(path), "%s/input.ply", directory);
    int fd = open(path, O_CREAT | O_EXCL | O_WRONLY, 0600);
    if (fd < 0) { rmdir(directory); return 0; }
    int written = 1;
    for (size_t offset = 0; offset < size;) {
        ssize_t count = write(fd, data + offset, size - offset);
        if (count <= 0) { written = 0; break; }
        offset += (size_t)count;
    }
    if (close(fd) != 0) written = 0;

    size_t *node_tags = NULL, *triangle_tags = NULL, *triangle_nodes = NULL;
    double *coords = NULL, *parameters = NULL;
    size_t node_count = 0, coord_count = 0, parameter_count = 0;
    size_t triangle_count = 0, triangle_node_count = 0;
    int error = 0, initialized = 0, okay = 0;
    if (written) {
        gmshInitialize(0, NULL, 0, 0, &error);
        if (!error) {
            initialized = 1;
            gmshOptionSetNumber("General.Terminal", 0, &error);
        }
        if (!error) gmshOpen(path, &error);
        if (!error) {
            gmshModelMeshGetNodes(&node_tags, &node_count, &coords, &coord_count,
                                  &parameters, &parameter_count, -1, -1, 0, 0,
                                  &error);
        }
        if (!error && coord_count == 3 * node_count) {
            gmshModelMeshGetElementsByType(2, &triangle_tags, &triangle_count,
                                           &triangle_nodes, &triangle_node_count,
                                           -1, 0, 1, &error);
        }
        if (!error && coord_count == 3 * node_count &&
            triangle_node_count == 3 * triangle_count) {
            double x_sum = 0.0;
            for (size_t i = 0; i < node_count; ++i) x_sum += coords[3 * i];
            if (isfinite(x_sum)) {
                result->vertices = node_count;
                result->triangles = triangle_count;
                result->triangle_nodes = triangle_node_count;
                result->x_sum = x_sum;
                okay = 1;
            }
        }
    }
    gmshFree(node_tags);
    gmshFree(coords);
    gmshFree(parameters);
    gmshFree(triangle_tags);
    gmshFree(triangle_nodes);
    if (initialized) { int finalize_error = 0; gmshFinalize(&finalize_error); }
    unlink(path);
    rmdir(directory);
    return okay;
}
