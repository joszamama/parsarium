#ifndef PARSARIUM_MDAL_PLY_HARNESS_H
#define PARSARIUM_MDAL_PLY_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_ply_result {
    int vertices;
    int faces;
    /* Vertex indices of the first face (malloc'd, index_count entries); NULL
     * with index_count 0 when the mesh has no faces. */
    int *indices;
    int index_count;
};

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result);

void parsarium_free_result(struct parsarium_ply_result *result);

#endif
