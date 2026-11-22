#ifndef PARSARIUM_LIBAGAR_PLY_HARNESS_H
#define PARSARIUM_LIBAGAR_PLY_HARNESS_H

#include <stddef.h>
#include <stdint.h>

struct parsarium_ply_result {
    unsigned vertices;
    unsigned faces;
    /* Vertices of the first facet in Agar's facet table (SG facets have 3 or 4),
     * as input vertex numbers; -1 for Agar's reserved vertex 0, which no input
     * vertex maps to. face_size is 0 when the object has no facets. */
    int face[4];
    unsigned face_size;
};

int parsarium_parse_ply(const uint8_t *data, size_t size,
                        struct parsarium_ply_result *result);

/* Agar's error string (AG_GetError) after a failed parse, or NULL. */
const char *parsarium_last_error(void);

#endif
